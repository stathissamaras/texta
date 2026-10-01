from django.shortcuts import redirect, render
from django.templatetags.static import static

from .materials import BY_CODE, KENTRIKA, PLAINA, SEAT
from .services.seat_render import get_or_create_render, get_or_create_swatch


def configurator(request):
    """Ανοίγει με το λευκό κάθισμα - από την ίδια διαδικασία με τα υπόλοιπα,
    ώστε να έχει ακριβώς τις ίδιες διαστάσεις."""
    return render(request, "configurator.html", {
        "seat": SEAT,
        "white_image": get_or_create_render(SEAT, None, None),
        "kentrika": [dict(m, swatch=get_or_create_swatch(m)) for m in KENTRIKA],
        "plaina": [dict(m, swatch=get_or_create_swatch(m)) for m in PLAINA],
    })


def eikona(request, kentrika, plaina):
    """Η εικόνα για έναν συνδυασμό. Ο κωδικός 'white' σημαίνει άβαφη ζώνη."""
    k = BY_CODE.get(kentrika)
    p = BY_CODE.get(plaina)
    return redirect(get_or_create_render(SEAT, k, p))