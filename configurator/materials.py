"""Το χρωματολόγιο. Διαβάζεται αυτόματα από τους φακέλους -
ρίχνεις μια φωτό μέσα και εμφανίζεται στη λίστα."""

from pathlib import Path

from django.conf import settings

SEAT = {
    "slug": "kathisma",
    "name": "Κάθισμα οδηγού",
    "layers_dir": "images/seats/kathisma",
    "white": "images/seats/kathisma/preview_white.png",
}

# Πόσες φορές επαναλαμβάνεται το δείγμα πάνω σε ολόκληρο το ξεδίπλωμα του
# καλύμματος. ΜΕΓΑΛΥΤΕΡΟ νούμερο = ΨΙΛΟΤΕΡΟ σχέδιο. Είναι το αντίστροφο
# από το παλιό tile_scale, γι' αυτό οι τιμές είναι σε άλλη τάξη μεγέθους.
REPEAT_FABRIC = 18
REPEAT_LEATHER = 9

# Πόσο μικρό κομμάτι της φωτογραφίας δείχνει το τετραγωνάκι του δειγματολογίου.
# 1 = ολόκληρη η φωτό. Στις δερματίνες, που είναι 2360 pixel, ολόκληρη
# σμικρύνεται τόσο που χάνεται το ανάγλυφο και μένει σκέτο χρώμα.
SWATCH_DIV_FABRIC = 1
SWATCH_DIV_LEATHER = 3

_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def _scan(folder: str, prefix: str, repeat: float, swatch_div: int) -> list[dict]:
    """Διαβάζει έναν φάκελο και φτιάχνει τη λίστα υλικών."""
    root = Path(settings.BASE_DIR) / "static" / "images" / "seats" / folder
    return [
        {
            "code": f"{prefix}-{p.stem}",
            "name": p.stem,
            "tile": f"images/seats/{folder}/{p.name}",
            "repeat": repeat,
            "swatch_div": swatch_div,
        }
        for p in sorted(root.iterdir())
        if p.suffix.lower() in _EXT
    ]


KENTRIKA = _scan("fabric", "K", REPEAT_FABRIC, SWATCH_DIV_FABRIC)
PLAINA = _scan("leathers", "P", REPEAT_LEATHER, SWATCH_DIV_LEATHER)

BY_CODE = {m["code"]: m for m in KENTRIKA + PLAINA}