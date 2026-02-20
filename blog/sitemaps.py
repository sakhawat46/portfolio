from django.contrib.sitemaps import Sitemap

from .models import BlogPost


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.published()

    def lastmod(self, obj):
        return obj.updated_at
