from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """Η φόρμα επικοινωνίας της αρχικής."""

    name = forms.CharField(
        max_length=120, label=_("Επωνυμία"),
        widget=forms.TextInput(attrs={"placeholder": _("Επωνυμία")}),
        error_messages={"required": _("Συμπληρώστε την επωνυμία σας.")},
    )
    phone = forms.CharField(
        max_length=40, required=False, label=_("Τηλέφωνο"),
        widget=forms.TextInput(attrs={"type": "tel", "placeholder": _("Τηλέφωνο")}),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"placeholder": _("Το email σας")}),
        error_messages={
            "required": _("Συμπληρώστε το email σας."),
            "invalid": _("Το email δεν φαίνεται σωστό."),
        },
    )
    subject = forms.CharField(
        max_length=150, required=False, label=_("Θέμα"),
        widget=forms.TextInput(attrs={"placeholder": _("Θέμα")}),
    )
    message = forms.CharField(
        max_length=4000, label=_("Μήνυμα"),
        widget=forms.Textarea(attrs={"placeholder": _("Το μήνυμά σας")}),
        error_messages={"required": _("Γράψτε μας το μήνυμά σας.")},
    )

    # Παγίδα για τα ρομπότ: κρύβεται με CSS, όχι με type=hidden.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError(_("Η υποβολή απορρίφθηκε."))
        return ""


class NewsletterForm(forms.Form):
    """Εγγραφή στο newsletter. Μόνο email - ό,τι άλλο ζητήσεις μειώνει τις εγγραφές."""

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            "placeholder": _("Email Here"),
            "autocomplete": "email",
        }),
        error_messages={
            "required": _("Συμπληρώστε το email σας."),
            "invalid": _("Το email δεν φαίνεται σωστό."),
        },
    )

    # Παγίδα για τα ρομπότ - κρύβεται με CSS, όχι με type=hidden.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError(_("Η υποβολή απορρίφθηκε."))
        return ""