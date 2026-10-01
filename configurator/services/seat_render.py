"""
Σύνθεση καλύμματος καθίσματος.

Αρχή 1: ο φωτισμός δεν υπολογίζεται εδώ, διαβάζεται. Το light_ratio.png λέει,
για κάθε pixel, πόσο φως έχει σε σχέση με το «κανονικό» της ζώνης του.
Το υλικό πολλαπλασιάζεται με αυτό.

Αρχή 2: το ύφασμα δεν πλακοστρώνεται πάνω στην οθόνη, μπαίνει πάνω στο
πατρόν. Τα uv_u/uv_v λένε, για κάθε pixel, σε ποιο σημείο του ξεδιπλωμένου
καλύμματος αντιστοιχεί. Έτσι η φορά του σχεδίου ακολουθεί το κάθε κομμάτι
και το ύφασμα κονταίνει σωστά εκεί που η επιφάνεια φεύγει σε φυγή.

Layers στο static/<layers_dir>/ :
    light_ratio.png      L      - ο φωτισμός, 0..255 = 0.0..2.0
    silhouette.png       L      - η διαφάνεια του καθίσματος
    mask_kentrika.png    RGBA   - alpha = η ζώνη των κεντρικών
    mask_plaina.png      RGBA   - alpha = η ζώνη των πλαϊνών
    mask_plastika.png    RGBA   - alpha = ο μηχανισμός, δεν βάφεται
    uv_u.png             L 16bit- η οριζόντια συντεταγμένη του πατρόν
    uv_v.png             L 16bit- η κατακόρυφη συντεταγμένη του πατρόν
    preview_white.png           - η αρχική λευκή εικόνα
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import cv2
import numpy as np
from django.conf import settings

# ---------------------------------------------------------------- παράμετροι

RENDER_VERSION = 15     # ΑΝΕΒΑΣΕ ΤΟ όταν αλλάξεις κάτι εδώ ή σε κάποιο υλικό.

OUTPUT_WIDTH = 1401    # πλάτος της εικόνας που βλέπει ο πελάτης
SWATCH_SIZE = 200      # πλευρά του μικρού δείγματος
JPEG_QUALITY = 88

TILE_MAX = 700          # μέγιστη πλευρά του πλακιδίου - πάνω από αυτό δεν
                        # κερδίζουμε τίποτα και η _flat_field αργεί
SHADOW_FLOOR = 0.22     # πόσο σκοτεινή γίνεται η βαθύτερη σκιά
LIGHT_MAX = 1.35        # πόσο φωτίζει η πιο φωτεινή ακμή
WHITE_BGR = (205, 205, 205)
PLASTIC_BGR = (34, 34, 36)

_LAYERS: dict[str, dict] = {}
_TILES: dict[str, np.ndarray] = {}


# ------------------------------------------------------------------ βοηθητικά

def _static(rel: str) -> Path:
    root = getattr(settings, "STATIC_ROOT", None)
    base = Path(root) if root else Path(settings.BASE_DIR) / "static"
    return base / rel


def _read(path: Path, flags: int) -> np.ndarray:
    img = cv2.imread(str(path), flags)
    if img is None:
        raise FileNotFoundError(f"Δεν βρέθηκε ή δεν διαβάζεται: {path}")
    return img


def _fit(a: np.ndarray, nearest: bool = False) -> np.ndarray:
    """Φέρνει ένα layer στο πλάτος εξόδου. Τα uv ΠΟΤΕ με μέσο όρο - μια
    ενδιάμεση τιμή στη ραφή δύο κομματιών δείχνει σε τελείως άλλο σημείο
    του πατρόν."""
    h, w = a.shape[:2]
    return cv2.resize(a, (OUTPUT_WIDTH, max(1, round(OUTPUT_WIDTH * h / w))),
                        interpolation=cv2.INTER_NEAREST if nearest else cv2.INTER_AREA)


def _load(layers_dir: str) -> dict:
    """Διαβάζει τα layers μία φορά και προϋπολογίζει ό,τι δεν εξαρτάται
    από το υλικό. Μένουν στη μνήμη του process."""
    if layers_dir in _LAYERS:
        return _LAYERS[layers_dir]

    base = _static(layers_dir)
    ratio = _fit(_read(base / "light_ratio.png", cv2.IMREAD_GRAYSCALE)).astype(np.float32) / 255 * 2
    alpha = _fit(_read(base / "silhouette.png", cv2.IMREAD_GRAYSCALE)).astype(np.float32) / 255
    mc, ms, mp = [
        _fit(_read(base / f"mask_{n}.png", cv2.IMREAD_UNCHANGED)[:, :, 3]).astype(np.float32) / 255
        for n in ("kentrika", "plaina", "plastika")
    ]
    u = _fit(_read(base / "uv_u.png", cv2.IMREAD_UNCHANGED), True).astype(np.float32) / 65535
    v = _fit(_read(base / "uv_v.png", cv2.IMREAD_UNCHANGED), True).astype(np.float32) / 65535

    # Ο φωτισμός είναι καθαρός πολλαπλασιαστής: κάτω από 1 σκιά, πάνω από 1 φως.
    # Τίποτα δεν προστίθεται, άρα κανένα υλικό δεν μπορεί να ασπρίσει.
    light = np.clip(SHADOW_FLOOR + (1 - SHADOW_FLOOR) * ratio, 0, LIGHT_MAX)

    data = dict(shape=ratio.shape, alpha=alpha, mc=mc, ms=ms, mp=mp, light=light, u=u, v=v)
    _LAYERS[layers_dir] = data
    return data


def _flat_field(t: np.ndarray) -> np.ndarray:
    """Αφαιρεί τον φωτισμό που είναι ήδη «ψημένος» μέσα στη φωτογραφία του
    υφάσματος - αλλιώς η σκιά της φωτό επαναλαμβάνεται σε κάθε πλακίδιο."""
    g = t.mean(2)
    lo = cv2.GaussianBlur(g, (0, 0), max(t.shape[:2]) / 7.0)
    return np.clip(t * (g.mean() / np.maximum(lo, 1e-3))[..., None], 0, 255)


BLEND = 0.14   # πόσο πλατιά είναι η λωρίδα που σβήνει στην ένωση


def _seamless(t: np.ndarray) -> np.ndarray:
    """Κάνει το πλακίδιο να κουμπώνει με τον εαυτό του: η κάθε άκρη σβήνει
    σταδιακά μέσα στην απέναντι, οπότε το πλακόστρωμα δεν αφήνει γραμμές."""
    h, w = t.shape[:2]
    bx, by = max(2, int(w * BLEND)), max(2, int(h * BLEND))

    a = np.linspace(0, 1, bx, dtype=np.float32)[None, :, None]
    out = t[:, :w - bx].copy()
    out[:, :bx] = t[:, :bx] * a + t[:, w - bx:] * (1 - a)

    b = np.linspace(0, 1, by, dtype=np.float32)[:, None, None]
    res = out[:h - by].copy()
    res[:by] = out[:by] * b + out[h - by:] * (1 - b)
    return res


def _block(tile_rel: str) -> np.ndarray:
    """ΟΛΟΚΛΗΡΗ η φωτογραφία γίνεται πλακίδιο, στη μεγαλύτερη ανάλυση που
    έχει νόημα. Πόσο μεγάλο θα φανεί το ορίζει το repeat, όχι η σμίκρυνση."""
    if tile_rel in _TILES:
        return _TILES[tile_rel]

    im = _read(_static(tile_rel), cv2.IMREAD_COLOR).astype(np.float32)
    h, w = im.shape[:2]
    s = min(1.0, TILE_MAX / max(h, w))
    if s < 1.0:
        im = cv2.resize(im, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)

    block = _seamless(_flat_field(im))
    _TILES[tile_rel] = block
    return block


def _on_pattern(tile_rel: str, repeat: float, L: dict) -> np.ndarray:
    """Στρώνει το ύφασμα πάνω στο πατρόν. Το repeat λέει πόσες φορές
    επαναλαμβάνεται το δείγμα σε ολόκληρο το ξεδίπλωμα - μεγαλύτερο
    νούμερο, ψιλότερο σχέδιο."""
    block = _block(tile_rel)
    bh, bw = block.shape[:2]
    # Το δείγμα πρέπει να μπει στην ίδια φυσική κλίμακα και στους δύο άξονες.
    # Αν η φωτογραφία δεν είναι τετράγωνη και βάλουμε παντού το ίδιο repeat,
    # το σχέδιο πλακώνεται - στα 16:9 δείγματα κατά 1,78 φορές.
    ru, rv = repeat, repeat * bw / bh
    mx = ((L["u"] * ru) % 1.0 * bw).astype(np.float32)
    my = ((L["v"] * rv) % 1.0 * bh).astype(np.float32)
    return cv2.remap(block, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)


# -------------------------------------------------------------------- σύνθεση

def render_seat(seat: dict, kentrika: dict | None, plaina: dict | None) -> np.ndarray:
    """Επιστρέφει BGRA εικόνα. Ό,τι υλικό είναι None μένει λευκό."""
    L = _load(seat["layers_dir"])
    h, w = L["shape"]

    def zone(material):
        if material is None:
            return np.broadcast_to(np.float32(WHITE_BGR), (h, w, 3))
        return _on_pattern(material["tile"], material["repeat"], L)

    color = (zone(kentrika) * L["mc"][..., None]
             + zone(plaina) * L["ms"][..., None]
             + np.float32(PLASTIC_BGR) * L["mp"][..., None])

    comp = np.clip(color * L["light"][..., None], 0, 255)
    return np.dstack([comp, L["alpha"] * 255]).astype(np.uint8)


def get_or_create_render(seat: dict, kentrika: dict | None, plaina: dict | None) -> str:
    """Το URL της εικόνας. Κάθε συνδυασμός υπολογίζεται μία φορά στη ζωή του."""
    a = kentrika["code"] if kentrika else "white"
    b = plaina["code"] if plaina else "white"
    digest = hashlib.sha1(f'v{RENDER_VERSION}|{seat["slug"]}|{a}|{b}'.encode()).hexdigest()[:16]

    rel = f'renders/{seat["slug"]}/{digest}.jpg'
    path = Path(settings.MEDIA_ROOT) / rel

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        img = render_seat(seat, kentrika, plaina)
        # Ένωση με λευκό φόντο. Το JPEG είναι μερικές εκατοντάδες KB αντί για
        # μερικά MB του PNG, και ο πελάτης το κατεβάζει σε κάθε κλικ.
        alpha = img[:, :, 3:4].astype(np.float32) / 255
        flat = (img[:, :, :3].astype(np.float32) * alpha + 255 * (1 - alpha)).astype(np.uint8)
        cv2.imwrite(str(path), flat, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])

    return settings.MEDIA_URL + rel


def get_or_create_swatch(material: dict) -> str:
    """Το URL του μικρού δείγματος για τη λίστα. Φτιάχνεται μία φορά.
    Χωρίς αυτό ο browser κατεβάζει τα αρχικά αρχεία - πάνω από 20 MB."""
    digest = hashlib.sha1(material["tile"].encode()).hexdigest()[:16]
    rel = f"swatches/{digest}.jpg"
    path = Path(settings.MEDIA_ROOT) / rel

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        im = _read(_static(material["tile"]), cv2.IMREAD_COLOR)
        h, w = im.shape[:2]
        s = min(h, w) // material.get("swatch_div", 1)
        crop = im[(h - s) // 2:(h + s) // 2, (w - s) // 2:(w + s) // 2]
        cv2.imwrite(str(path),
                    cv2.resize(crop, (SWATCH_SIZE, SWATCH_SIZE), interpolation=cv2.INTER_AREA),
                    [cv2.IMWRITE_JPEG_QUALITY, 85])

    return settings.MEDIA_URL + rel