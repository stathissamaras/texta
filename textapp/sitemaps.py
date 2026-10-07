from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category


class StaticViewSitemap(Sitemap):
    """Σελίδες χωρίς εγγραφή στη βάση."""

    changefreq = "monthly"
    protocol = "https"
    i18n = True          # μία εγγραφή ανά γλώσσα
    alternates = True    # hreflang μέσα στο sitemap
    x_default = False

    def items(self):
        return ["textapp:home", "textapp:facilities", "textapp:legal"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "textapp:home" else 0.6


class CategorySitemap(Sitemap):
    """Οι κατηγορίες υλικών. Το lastmod βγαίνει από το updated_at."""

    changefreq = "monthly"
    priority = 0.8
    protocol = "https"
    i18n = True
    alternates = True
    x_default = False    # βλ. σχόλιο στο StaticViewSitemap

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at