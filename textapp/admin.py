import csv
from django.utils.html import format_html
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from .models import Category, ContactMessage, ItemView, Product, Subscriber

# ------------------------------------------------------------ βοηθητικά

def export_csv(modeladmin, request, queryset):
    """Κατεβάζει τα επιλεγμένα ως CSV. Το utf-8-sig είναι απαραίτητο,
    αλλιώς το Excel δείχνει τα ελληνικά σαν κινέζικα."""
    fields = [f.name for f in modeladmin.model._meta.fields]
    name = modeladmin.model._meta.verbose_name_plural

    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="{name}.csv"'
    response.write("\ufeff")                       # BOM για το Excel

    writer = csv.writer(response, delimiter=";")   # ; γιατί το ελληνικό Excel έτσι διαβάζει
    writer.writerow([modeladmin.model._meta.get_field(f).verbose_name for f in fields])
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in fields])
    return response


export_csv.short_description = _("Εξαγωγή σε CSV (Excel)")


def _thumb(image, size=110):
    """Μικρογραφία για το admin, πάντα τετράγωνη."""
    if not image:
        return "-"
    return format_html(
        '<img src="{}" style="width:{}px;height:{}px;object-fit:cover;'
        'border:1px solid #ddd;border-radius:4px;margin-right:6px;">',
        image.url, size, size,
    )


# ------------------------------------------------------------ ΚΑΤΗΓΟΡΙΕΣ

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name_el", "slug", "product_count", "is_active", "order")
    list_display_links = ("name_el",)
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("name_el", "name_en", "slug")
    prepopulated_fields = {"slug": ("name_el",)}
    ordering = ("order", "name_el")
    readonly_fields = ("preview_all",)

    @admin.display(description=_("Όσες φωτό έχεις βάλει"))
    def preview_all(self, obj):
        imgs = [obj.image_main] + obj.gallery
        parts = [_thumb(i, 70) for i in imgs if i]
        return mark_safe("".join(parts)) if parts else "-"

    fieldsets = (
        (_("Ταυτότητα"), {
            "fields": ("slug", ("name_el", "name_en"),
                        ("subtitle_el", "subtitle_en"))
        }),
        (_("Κείμενα"), {
            "fields": (("short_el", "short_en"),
                        ("intro_el", "intro_en"),
                        ("intro2_el", "intro2_en"),
                        ("intro3_el", "intro3_en"),
                        ("intro4_el", "intro4_en"),
                        ("intro5_el", "intro5_en"),
                        ("intro6_el", "intro6_en"),
                        ("intro7_el", "intro7_en"),
                        ("intro8_el", "intro8_en"))
        }),
        (_("SEO"), {
            "fields": (("meta_description_el", "meta_description_en"),),
            "description": _("Έως 160 χαρακτήρες. Αν μείνει κενό μπαίνει το σύντομο κείμενο.")
        }),
        (_("Φωτογραφίες"), {
            "fields": ("preview_all",
                        ("image_main", "image_2"),
                        ("image_3", "image_4"),
                        ("image_5", "image_6"),
                        ("image_7", "image_8"),
                        ("image_9", "image_10"))
        }),
        (_("Εμφάνιση"), {
            "fields": ("is_active", "order")
        }),
    )

    @admin.display(description=_("Κωδικοί"))
    def product_count(self, obj):
        return obj.products.count()

    @admin.display(description=_("Φωτό"))
    def thumb(self, obj):
        return _thumb(obj.image_main, 46)


# ------------------------------------------------------------ ΠΡΟΪΟΝΤΑ

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "code", "category", "name_el", "is_active", "order")
    list_display_links = ("code",)
    list_editable = ("is_active", "order")
    list_filter = ("category", "is_active", "bielasticity")
    list_select_related = ("category",)
    search_fields = ("code", "name_el", "name_en")
    prepopulated_fields = {"slug": ("name_el",)}
    ordering = ("order", "code")
    readonly_fields = ("preview_main", "preview_2", "preview_3",
                        "preview_4", "preview_5")

    fieldsets = (
        (_("Ταυτότητα"), {
            "fields": ("category", "code", "slug", ("name_el", "name_en"),
                        ("subtitle_el", "subtitle_en"))
        }),
        (_("Κείμενα"), {
            "fields": (("short_el", "short_en"),
                        ("description_el", "description_en"),
                        ("description2_el", "description2_en"),
                        ("description3_el", "description3_en"),
                        ("description4_el", "description4_en"))
        }),
        (_("SEO"), {
            "fields": (("meta_description_el", "meta_description_en"),),
            "description": _("Έως 160 χαρακτήρες. Αν μείνει κενό μπαίνει το σύντομο κείμενο.")
        }),
        (_("Τεχνικά χαρακτηριστικά"), {
            "fields": (("composition_el", "composition_en"),
                        "weight", "density", "thickness", "foam",
                        ("color_el", "color_en"),
                        ("pattern_el", "pattern_en"),
                        "bielasticity")
        }),
        (_("Φωτογραφίες"), {
            "fields": (("image_main", "preview_main"),
                        ("image_2", "preview_2"),
                        ("image_3", "preview_3"),
                        ("image_4", "preview_4"),
                        ("image_5", "preview_5"))
        }),
        (_("Εμφάνιση"), {
            "fields": ("is_active", "order")
        }),
    )

    @admin.display(description=_("Φωτό"))
    def thumb(self, obj):
        return _thumb(obj.image_main, 46)

    @admin.display(description=_("Προεπισκόπηση"))
    def preview_main(self, obj):
        return _thumb(obj.image_main)

    @admin.display(description=_("Προεπισκόπηση"))
    def preview_2(self, obj):
        return _thumb(obj.image_2)

    @admin.display(description=_("Προεπισκόπηση"))
    def preview_3(self, obj):
        return _thumb(obj.image_3)

    @admin.display(description=_("Προεπισκόπηση"))
    def preview_4(self, obj):
        return _thumb(obj.image_4)

    @admin.display(description=_("Προεπισκόπηση"))
    def preview_5(self, obj):
        return _thumb(obj.image_5)


# ------------------------------------------------------------ ΕΠΙΚΟΙΝΩΝΙΑ

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Μόνο ανάγνωση. Τίποτα δεν προστίθεται ή αλλάζει από εδώ."""

    list_display = ("created_at", "name", "email", "phone", "country", "subject")
    list_filter = ("country", "language", "utm_source", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    actions = [export_csv]

    readonly_fields = [f.name for f in ContactMessage._meta.fields]

    fieldsets = (
        (_("Ποιος έγραψε"), {
            "fields": ("created_at", "name", "email", "phone")
        }),
        (_("Τι έγραψε"), {
            "fields": ("subject", "message")
        }),
        (_("Από πού"), {
            "fields": ("country", "city", "language", "ip_address",
                        "referrer", ("utm_source", "utm_medium", "utm_campaign"),
                        "user_agent", "consent_at")
        }),
    )

    def has_add_permission(self, request):
        return False


# ------------------------------------------------------------ NEWSLETTER

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "confirmed_at", "unsubscribed_at",
                    "source", "language")
    list_filter = ("source", "language", "confirmed_at", "unsubscribed_at")
    search_fields = ("email",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    actions = [export_csv]

    readonly_fields = ("created_at", "ip_address")

    def has_add_permission(self, request):
        return False


# ------------------------------------------------------------ ΠΡΟΒΟΛΕΣ

@admin.register(ItemView)
class ItemViewAdmin(admin.ModelAdmin):
    """Μόνο ανάγνωση. Για τα στατιστικά: φιλτράρεις είδος και βλέπεις
    ποια δείγματα ανοίγουν περισσότερο."""

    list_display = ("created_at", "kind", "item", "language")
    list_filter = ("kind", "language", "created_at")
    search_fields = ("item",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    readonly_fields = [f.name for f in ItemView._meta.fields]

    def has_add_permission(self, request):
        return False
