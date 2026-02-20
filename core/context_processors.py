from .models import SiteSettings


def site_settings(request):
    return {
        "site_settings": SiteSettings.objects.prefetch_related("social_links").first(),
    }
