from django.conf import settings
from django.urls import translate_url


def seo(request):
    """Κανονικό URL και εναλλακτικές γλώσσες για τα <link> του base.html.

    Το translate_url μετατρέπει το τρέχον URL στο αντίστοιχο κάθε γλώσσας,
    σεβόμενο τα i18n_patterns - δεν κάνουμε χειροκίνητη αντικατάσταση prefix.
    """
    current = request.build_absolute_uri(request.path)
    return {
        'canonical_url': current,
        'alternate_urls': [
            (code, translate_url(current, code))
            for code, _name in settings.LANGUAGES
        ],
    }