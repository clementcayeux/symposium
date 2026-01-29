from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    """Sitemap pour les pages principales accessibles via une URL unique"""
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        # On liste les noms (name=...) définis dans tes fichiers urls.py
        return ['index', 'equipe']

    def location(self, item):
        return reverse(item)