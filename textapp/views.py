from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from django.views.generic import DetailView, TemplateView

from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .emails import read_token, send_newsletter_confirmation, send_newsletter_notice
from .forms import ContactForm, NewsletterForm
from .models import Category, Subscriber


class HomeView(FormView):
    """Η αρχική. Είναι FormView ώστε, αν η φόρμα έχει λάθος, η σελίδα να
    ξαναδείχνεται με ό,τι είχε πληκτρολογήσει ο επισκέπτης."""

    template_name = "home.html"
    form_class = ContactForm

    def get_success_url(self):
        return reverse("textapp:home") + "#contact"

    def form_valid(self, form):
        d = form.cleaned_data
        body = "\n".join([
            f"Επωνυμία: {d['name']}",
            f"Τηλέφωνο: {d['phone'] or '-'}",
            f"Email: {d['email']}",
            "",
            d["message"],
        ])

        EmailMessage(
            subject=f"[JB Car Textile] {d['subject'] or 'Μήνυμα από τη σελίδα'}",
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[d["email"]],      # απαντάς με ένα κλικ στον πελάτη
        ).send(fail_silently=False)

        messages.success(self.request,
                        _("Το μήνυμά σας στάλθηκε. Θα επικοινωνήσουμε σύντομα."))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Ελέγξτε τα πεδία με κόκκινο."))
        return super().form_invalid(form)


def _client_ip(request):
    """Πίσω από reverse proxy η πραγματική IP είναι στο X-Forwarded-For."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@require_POST
def newsletter_subscribe(request):
    """Δέχεται μόνο POST από το footer. Επιστρέφει πάντα στη σελίδα
    που ήρθε, με μήνυμα."""

    form = NewsletterForm(request.POST)

    if not form.is_valid():
        messages.error(request, _("Το email δεν φαίνεται σωστό."))
        return redirect("textapp:newsletter_sent")

    email = form.cleaned_data["email"].lower()
    ip = _client_ip(request)

    # Ένα αίτημα ανά λεπτό ανά IP - φράγμα σε αυτόματες υποβολές.
    if cache.get(f"newsletter:{ip}"):
        messages.error(request, _("Δοκιμάστε ξανά σε λίγο."))
        return redirect("textapp:newsletter_sent")
    cache.set(f"newsletter:{ip}", 1, 60)

    subscriber, created = Subscriber.objects.get_or_create(
        email=email,
        defaults={
            "language": request.LANGUAGE_CODE,
            "source": Subscriber.Source.FOOTER,
            "ip_address": ip,
        },
    )

    if subscriber.confirmed_at and not subscriber.unsubscribed_at:
        messages.info(request, _("Το email σας είναι ήδη εγγεγραμμένο."))
        return redirect("textapp:newsletter_sent")

    # Αν είχε απεγγραφεί και ξαναγράφεται, καθαρίζουμε την απεγγραφή.
    if subscriber.unsubscribed_at:
        subscriber.unsubscribed_at = None
        subscriber.save(update_fields=["unsubscribed_at"])

    send_newsletter_confirmation(request, subscriber)
    messages.success(request,
                        _("Σας στείλαμε email επιβεβαίωσης. Ελέγξτε τα εισερχόμενά σας."))
    return redirect("textapp:newsletter_sent")


def newsletter_confirm(request, token):
    """Το link που πατάει ο επισκέπτης στο email."""
    email = read_token(token)
    if not email:
        return render(request, "newsletter_result.html",
                        {"ok": False, "reason": "invalid"})

    try:
        subscriber = Subscriber.objects.get(email=email)
    except Subscriber.DoesNotExist:
        return render(request, "newsletter_result.html",
                        {"ok": False, "reason": "missing"})

    if not subscriber.confirmed_at:
        subscriber.confirm()
        send_newsletter_notice(subscriber)      # ειδοποίηση στο info@

    return render(request, "newsletter_result.html",
                    {"ok": True, "email": email})


def newsletter_unsubscribe(request, token):
    """Link απεγγραφής - μπαίνει σε κάθε newsletter που θα σταλεί."""
    email = read_token(token, max_age=60 * 60 * 24 * 365 * 5)   # δεν λήγει πρακτικά
    if not email:
        return render(request, "newsletter_result.html",
                        {"ok": False, "reason": "invalid"})

    Subscriber.objects.filter(email=email, unsubscribed_at__isnull=True).update(
        unsubscribed_at=timezone.now()
    )
    return render(request, "newsletter_result.html",
                    {"ok": True, "unsubscribed": True, "email": email})


def newsletter_sent(request):
    """Η σελίδα που βλέπει ο επισκέπτης αφού πατήσει SUBSCRIBE."""
    return render(request, "newsletter_result.html", {"sent": True})


class CategoryDetailView(DetailView):
    """Η σελίδα ενός είδους. Κάθε είδος έχει δικό του template,
    με όνομα το slug του: templates/categories/<slug>.html"""

    model = Category
    context_object_name = "category"

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def get_template_names(self):
        return [f"categories/{self.object.slug}.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object.products.filter(is_active=True)
        context["categories"] = Category.objects.filter(is_active=True)
        return context


class FacilitiesView(TemplateView):
    """Στατική σελίδα εξοπλισμού. Οι φωτό μπαίνουν από τα static."""

    template_name = "facilities.html"


class LegalView(TemplateView):
    """Όροι χρήσης, πολιτική απορρήτου και δικαιώματα GDPR σε μία σελίδα."""

    template_name = "legal.html"