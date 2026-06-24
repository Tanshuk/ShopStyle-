"""
Site-wide context processor — safe version.
"""
from django.conf import settings


def site_context(request):
    """
    Provides site name and tagline to every template.
    """
    try:
        site_name    = getattr(settings, 'SITE_NAME', 'ShopStyle')
        site_tagline = getattr(settings, 'SITE_TAGLINE', 'Fashion for Everyone')
    except Exception:
        site_name    = 'ShopStyle'
        site_tagline = 'Fashion for Everyone'

    return {
        'SITE_NAME':      site_name,
        'SITE_TAGLINE':   site_tagline,
        'top_categories': [],
        'popular_brands': [],
    }