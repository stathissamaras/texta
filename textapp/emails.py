"""Αποστολή email. Κάθε μήνυμα έχει .txt και .html εκδοχή:
το .txt το διαβάζουν τα φίλτρα spam και οι παλιοί clients."""

from django.conf import settings
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

SALT = "newsletter"
TOKEN_MAX_AGE = 60 * 60 * 24 * 7   # μία εβδομάδα για να επιβεβαιώσει


def make_token(email: str) -> str:
    """Υπογεγραμμένο token - δεν χρειάζεται στήλη στη βάση."""
    return signing.dumps(email, salt=SALT)


def read_token(token: str, max_age: int = TOKEN_MAX_AGE) -> str | None:
    """Επιστρέφει το email ή None αν το token είναι πλαστό ή έληξε."""
    try:
        return signing.loads(token, salt=SALT, max_age=max_age)
    except signing.BadSignature:
        return None


def _send(subject, template_base, context, to):
    """Στέλνει το ίδιο μήνυμα σε text και html."""
    text = render_to_string(f"emails/{template_base}.txt", context)
    html = render_to_string(f"emails/{template_base}.html", context)

    msg = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, to)
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)


def send_newsletter_confirmation(request, subscriber):
    """Στον επισκέπτη: link επιβεβαίωσης."""
    token = make_token(subscriber.email)
    url = request.build_absolute_uri(
        reverse("textapp:newsletter_confirm", args=[token])
    )
    _send(
        subject=_("Επιβεβαιώστε την εγγραφή σας - JB Car Textile"),
        template_base="newsletter_confirm",
        context={
            "confirm_url": url,
            "email": subscriber.email,
        },
        to=[subscriber.email],
    )


def send_newsletter_notice(subscriber):
    """Στην επιχείρηση: νέα εγγραφή."""
    _send(
        subject=f"[JB Car Textile] Νέα εγγραφή newsletter: {subscriber.email}",
        template_base="newsletter_notice",
        context={"subscriber": subscriber},
        to=[settings.CONTACT_EMAIL],
    )
