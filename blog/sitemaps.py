from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated
    