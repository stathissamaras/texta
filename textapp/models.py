from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from .storage import OverwriteStorage


class TranslatedFieldsMixin:
    """Επιστρέφει το πεδίο της τρέχουσας γλώσσας με fallback στα ελληνικά.
    Χρήση στο template: {{ product.name }} - όχι {{ product.name_el }}."""

    def _t(self, field: str) -> str:
        lang = (get_language() or "el")[:2]
        return getattr(self, f"{field}_{lang}", "") or getattr(self, f"{field}_el", "")


class Category(TranslatedFieldsMixin, models.Model):
    """Το είδος υφάσματος - 6 εγγραφές: πικέ, βελουτέ, suede, πετσέτα,
    ζακάρ, δερματίνες. Κάθε είδος έχει δική του σελίδα και από κάτω
    κρέμονται οι κωδικοί (Product)."""

    slug = models.SlugField(_("Slug"), max_length=60, unique=True,
                            help_text=_("Μπαίνει στο URL, π.χ. pike-ouranou"))

    name_el = models.CharField(_("Όνομα (ΕΛ)"), max_length=120)
    name_en = models.CharField(_("Όνομα (ΕΝ)"), max_length=120, blank=True)

    subtitle_el = models.CharField(_("Υπότιτλος (ΕΛ)"), max_length=120, blank=True)
    subtitle_en = models.CharField(_("Υπότιτλος (ΕΝ)"), max_length=120, blank=True)

    short_el = models.TextField(_("Σύντομο κείμενο (ΕΛ)"), blank=True,
                                help_text=_("Εμφανίζεται στην κάρτα του είδους"))
    short_en = models.TextField(_("Σύντομο κείμενο (ΕΝ)"), blank=True)

    intro_el = models.TextField(_("Γενικό κείμενο (ΕΛ)"), blank=True,
                                help_text=_("Η παρουσίαση στην κορυφή της σελίδας"))
    intro_en = models.TextField(_("Γενικό κείμενο (ΕΝ)"), blank=True)

    intro2_el = models.TextField(_("Γενικό κείμενο B (ΕΛ)"), blank=True)
    intro2_en = models.TextField(_("Γενικό κείμενο B (ΕΝ)"), blank=True)

    intro3_el = models.TextField(_("Γενικό κείμενο C (ΕΛ)"), blank=True)
    intro3_en = models.TextField(_("Γενικό κείμενο C (ΕΝ)"), blank=True)

    intro4_el = models.TextField(_("Γενικό κείμενο D (ΕΛ)"), blank=True)
    intro4_en = models.TextField(_("Γενικό κείμενο D (ΕΝ)"), blank=True)

    intro5_el = models.TextField(_("Γενικό κείμενο E (ΕΛ)"), blank=True)
    intro5_en = models.TextField(_("Γενικό κείμενο E (ΕΝ)"), blank=True)

    intro6_el = models.TextField(_("Γενικό κείμενο F (ΕΛ)"), blank=True)
    intro6_en = models.TextField(_("Γενικό κείμενο F (ΕΝ)"), blank=True)

    intro7_el = models.TextField(_("Γενικό κείμενο G (ΕΛ)"), blank=True)
    intro7_en = models.TextField(_("Γενικό κείμενο G (ΕΝ)"), blank=True)

    intro8_el = models.TextField(_("Γενικό κείμενο H (ΕΛ)"), blank=True)
    intro8_en = models.TextField(_("Γενικό κείμενο H (ΕΝ)"), blank=True)

    # --- SEO: αν μείνει κενό, το template πέφτει στο short ---
    meta_description_el = models.CharField(_("Meta description (ΕΛ)"),
                                            max_length=160, blank=True)
    meta_description_en = models.CharField(_("Meta description (ΕΝ)"),
                                            max_length=160, blank=True)

    # --- φωτογραφίες: γεμίζεις όσες θέλεις, οι κενές αγνοούνται ---
    image_main = models.ImageField(_("Κύρια φωτό"), upload_to="categories/",
                                    storage=OverwriteStorage(), blank=True)
    image_2 = models.ImageField(_("Φωτό 2"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_3 = models.ImageField(_("Φωτό 3"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_4 = models.ImageField(_("Φωτό 4"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_5 = models.ImageField(_("Φωτό 5"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_6 = models.ImageField(_("Φωτό 6"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_7 = models.ImageField(_("Φωτό 7"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_8 = models.ImageField(_("Φωτό 8"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_9 = models.ImageField(_("Φωτό 9"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)
    image_10 = models.ImageField(_("Φωτό 10"), upload_to="categories/",
                                storage=OverwriteStorage(), blank=True)

    is_active = models.BooleanField(_("Ενεργό"), default=True)
    order = models.PositiveSmallIntegerField(_("Σειρά"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Κατηγορία")
        verbose_name_plural = _("Κατηγορίες")
        ordering = ["order", "name_el"]

    def __str__(self):
        return self.name_el

    def get_absolute_url(self):
        return reverse("textapp:category", args=[self.slug])

    # --- Τα properties χρησιμοποιούνται στα templates ---
    @property
    def name(self):
        return self._t("name")

    @property
    def subtitle(self):
        return self._t("subtitle")

    @property
    def short(self):
        return self._t("short")

    @property
    def intro(self):
        return self._t("intro")

    @property
    def intro2(self):
        return self._t("intro2")

    @property
    def intro3(self):
        return self._t("intro3")

    @property
    def intro4(self):
        return self._t("intro4")

    @property
    def intro5(self):
        return self._t("intro5")

    @property
    def intro6(self):
        return self._t("intro6")

    @property
    def intro7(self):
        return self._t("intro7")

    @property
    def intro8(self):
        return self._t("intro8")

    @property
    def meta_description(self):
        return self._t("meta_description") or self._t("short")

    @property
    def gallery(self):
        """Όλες οι φωτό εκτός από την κύρια. Τα κενά πεδία πετιούνται."""
        fields = (self.image_2, self.image_3, self.image_4, self.image_5,
                    self.image_6, self.image_7, self.image_8, self.image_9,
                    self.image_10)
        return [img for img in fields if img]


class Product(TranslatedFieldsMixin, models.Model):
    """Τα είδη που παράγει η JB Car Textile. Κάθε κείμενο χωριστά σε ΕΛ και ΕΝ -
    η μετάφραση γράφεται με το χέρι, δεν παράγεται αυτόματα."""

    code = models.CharField(_("Κωδικός"), max_length=30, unique=True)
    slug = models.SlugField(_("Slug"), max_length=60, unique=True,
                            help_text=_("Μπαίνει στο URL, π.χ. ouranos-pike"))

    category = models.ForeignKey(Category, verbose_name=_("Είδος"),
                                on_delete=models.PROTECT,
                                related_name="products")

    name_el = models.CharField(_("Όνομα (ΕΛ)"), max_length=120)
    name_en = models.CharField(_("Όνομα (ΕΝ)"), max_length=120, blank=True)

    subtitle_el = models.CharField(_("Υπότιτλος (ΕΛ)"), max_length=120, blank=True,
                                    help_text=_("π.χ. Ουρανού, Cotton"))
    subtitle_en = models.CharField(_("Υπότιτλος (ΕΝ)"), max_length=120, blank=True)

    short_el = models.TextField(_("Σύντομο κείμενο (ΕΛ)"), blank=True,
                                help_text=_("Εμφανίζεται στις κάρτες της αρχικής"))
    short_en = models.TextField(_("Σύντομο κείμενο (ΕΝ)"), blank=True)

    meta_description_el = models.CharField(_("Meta description (ΕΛ)"),
                                            max_length=160, blank=True)
    meta_description_en = models.CharField(_("Meta description (ΕΝ)"),
                                            max_length=160, blank=True)

    description_el = models.TextField(_("Αναλυτικό κείμενο (ΕΛ)"), blank=True)
    description_en = models.TextField(_("Αναλυτικό κείμενο (ΕΝ)"), blank=True)

    description2_el = models.TextField(_("Αναλυτικό κείμενο B (ΕΛ)"), blank=True)
    description2_en = models.TextField(_("Αναλυτικό κείμενο B (ΕΝ)"), blank=True)

    description3_el = models.TextField(_("Αναλυτικό κείμενο C (ΕΛ)"), blank=True)
    description3_en = models.TextField(_("Αναλυτικό κείμενο C (ΕΝ)"), blank=True)

    description4_el = models.TextField(_("Αναλυτικό κείμενο D (ΕΛ)"), blank=True)
    description4_en = models.TextField(_("Αναλυτικό κείμενο D (ΕΝ)"), blank=True)

    # --- τεχνικά χαρακτηριστικά ---
    composition_el = models.CharField(_("Σύνθεση (ΕΛ)"), max_length=150, blank=True,
                                        help_text=_("π.χ. 100% πολυεστερικό νήμα"))
    composition_en = models.CharField(_("Σύνθεση (ΕΝ)"), max_length=150, blank=True)

    weight = models.CharField(_("Βάρος"), max_length=60, blank=True,
                                help_text=_("π.χ. 280 g/m²"))
    density = models.CharField(_("Πυκνότητα"), max_length=60, blank=True)
    thickness = models.CharField(_("Πάχος υλικού"), max_length=60, blank=True,
                                    help_text=_("π.χ. 0,9 mm"))
    foam = models.CharField(_("Αφρολέξ"), max_length=80, blank=True,
                            help_text=_("π.χ. 35kg - standard 0,6 mm (0,2-0,8 mm)"))

    color_el = models.CharField(_("Χρώματα (ΕΛ)"), max_length=150, blank=True)
    color_en = models.CharField(_("Χρώματα (ΕΝ)"), max_length=150, blank=True)
    pattern_el = models.CharField(_("Σχέδιο (ΕΛ)"), max_length=150, blank=True)
    pattern_en = models.CharField(_("Σχέδιο (ΕΝ)"), max_length=150, blank=True)

    bielasticity = models.BooleanField(_("Διελαστικότητα"), default=False,
                                        help_text=_("Εμφανίζει το icon bielasticity"))

    # --- φωτογραφίες: γεμίζεις όσες θέλεις, οι κενές αγνοούνται ---
    image_main = models.ImageField(_("Κύρια φωτό"), upload_to="products/", storage=OverwriteStorage(), blank=True)
    image_2 = models.ImageField(_("Φωτό 2"), upload_to="products/", storage=OverwriteStorage(), blank=True)
    image_3 = models.ImageField(_("Φωτό 3"), upload_to="products/", storage=OverwriteStorage(), blank=True)
    image_4 = models.ImageField(_("Φωτό 4"), upload_to="products/", storage=OverwriteStorage(), blank=True)
    image_5 = models.ImageField(_("Φωτό 5"), upload_to="products/", storage=OverwriteStorage(), blank=True)

    is_active = models.BooleanField(_("Ενεργό"), default=True)
    order = models.PositiveSmallIntegerField(_("Σειρά"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Προϊόν")
        verbose_name_plural = _("Προϊόντα")
        ordering = ["order", "code"]

    def __str__(self):
        return f"{self.code} - {self.name_el}"

    def get_absolute_url(self):
        return reverse("textapp:product", args=[self.category.slug, self.slug])

    # --- Τα properties χρησιμοποιούνται στα templates ---
    @property
    def name(self):
        return self._t("name")

    @property
    def subtitle(self):
        return self._t("subtitle")

    @property
    def short(self):
        return self._t("short")

    @property
    def description(self):
        return self._t("description")

    @property
    def description2(self):
        return self._t("description2")

    @property
    def description3(self):
        return self._t("description3")

    @property
    def description4(self):
        return self._t("description4")

    @property
    def composition(self):
        return self._t("composition")

    @property
    def color(self):
        return self._t("color")

    @property
    def pattern(self):
        return self._t("pattern")

    @property
    def gallery(self):
        """Μόνο οι φωτό που έχεις ανεβάσει - τα κενά πεδία πετιούνται."""
        fields = (self.image_main, self.image_2, self.image_3,
                    self.image_4, self.image_5)
        return [img for img in fields if img]

    @property
    def meta_description(self):
        return self._t("meta_description") or self._t("short")


class ContactMessage(models.Model):
    """Ό,τι έρχεται από τη φόρμα επικοινωνίας. Τα πεδία έχουν τα ίδια ονόματα
    με τη ContactForm, ώστε να περνάνε κατευθείαν."""

    # --- ίδια ονόματα με τη φόρμα ---
    name = models.CharField(_("Επωνυμία"), max_length=120)
    phone = models.CharField(_("Τηλέφωνο"), max_length=40, blank=True)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Θέμα"), max_length=150, blank=True)
    message = models.TextField(_("Μήνυμα"))

    # --- γεωγραφική θέση, από την IP ---
    country = models.CharField(_("Χώρα"), max_length=80, blank=True, db_index=True)
    city = models.CharField(_("Πόλη"), max_length=80, blank=True)

    # --- γεμίζουν από το view, με βάση το request ---
    language = models.CharField(_("Γλώσσα"), max_length=5, blank=True, db_index=True)
    ip_address = models.GenericIPAddressField(_("IP"), null=True, blank=True)
    user_agent = models.TextField(_("Συσκευή"), blank=True)
    referrer = models.URLField(_("Προέλευση"), max_length=500, blank=True)
    utm_source = models.CharField(_("UTM source"), max_length=100, blank=True, db_index=True)
    utm_medium = models.CharField(_("UTM medium"), max_length=100, blank=True)
    utm_campaign = models.CharField(_("UTM campaign"), max_length=100, blank=True)

    consent_at = models.DateTimeField(_("Συγκατάθεση"), null=True, blank=True)
    created_at = models.DateTimeField(_("Ημερομηνία"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Μήνυμα επικοινωνίας")
        verbose_name_plural = _("Μηνύματα επικοινωνίας")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.created_at:%d/%m/%Y}"


class Subscriber(models.Model):
    """Newsletter. Το confirmed_at γεμίζει μόνο μετά από κλικ στο email
    επιβεβαίωσης - χωρίς αυτό δεν στέλνουμε τίποτα (GDPR)."""

    class Source(models.TextChoices):
        FOOTER = "footer", _("Footer")
        CONTACT = "contact", _("Φόρμα επικοινωνίας")
        OTHER = "other", _("Άλλο")

    email = models.EmailField(_("Email"), unique=True)
    language = models.CharField(_("Γλώσσα"), max_length=5, blank=True)
    source = models.CharField(_("Προέλευση"), max_length=20,
                                choices=Source.choices, default=Source.FOOTER)

    confirmed_at = models.DateTimeField(_("Επιβεβαιώθηκε"), null=True, blank=True)
    unsubscribed_at = models.DateTimeField(_("Απεγγράφηκε"), null=True, blank=True)

    ip_address = models.GenericIPAddressField(_("IP"), null=True, blank=True)
    created_at = models.DateTimeField(_("Ημερομηνία"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Συνδρομητής")
        verbose_name_plural = _("Συνδρομητές")
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    @property
    def is_active(self) -> bool:
        return bool(self.confirmed_at) and not self.unsubscribed_at

    def confirm(self):
        self.confirmed_at = timezone.now()
        self.save(update_fields=["confirmed_at"])


class ItemView(models.Model):
    """Τι κοίταξε ο επισκέπτης. Μόνο προϊόντα και δείγματα υφασμάτων -
    τίποτα άλλο δεν καταγράφεται."""

    class Kind(models.TextChoices):
        CATEGORY = "category", _("Είδος")
        PRODUCT = "product", _("Προϊόν")
        SWATCH = "swatch", _("Δείγμα")

    kind = models.CharField(_("Είδος"), max_length=10,
                            choices=Kind.choices, db_index=True)
    item = models.CharField(_("Κωδικός"), max_length=120, db_index=True,
                            help_text=_("π.χ. 'ouranos-pike' ή 'K622'"))

    ip_address = models.GenericIPAddressField(_("IP"), null=True, blank=True)
    session_key = models.CharField(_("Session"), max_length=40, blank=True, db_index=True)
    language = models.CharField(_("Γλώσσα"), max_length=5, blank=True)
    created_at = models.DateTimeField(_("Ημερομηνία"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Προβολή")
        verbose_name_plural = _("Προβολές")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["kind", "item", "created_at"])]

    def __str__(self):
        return f"{self.item} ({self.created_at:%d/%m %H:%M})"
