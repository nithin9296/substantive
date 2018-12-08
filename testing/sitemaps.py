from django.contrib.sitemaps import Sitemap
from .models import samples
 
 
class samplesSitemap(Sitemap):    
    changefreq = "weekly"
    priority = 0.9
 
    def items(self):
        return samples.objects.all()
 