"""
Wishlist context processor — safe version with full exception handling.
"""


def wishlist_context(request):
    """
    Inject wishlist_count into every template.
    Returns 0 safely if anything goes wrong.
    """
    wishlist_count = 0

    try:
        if request.user.is_authenticated:
            # Lazy import to avoid AppRegistryNotReady errors
            from apps.wishlist.models import Wishlist
            wishlist_count = Wishlist.objects.filter(
                user=request.user
            ).count()
    except Exception:
        wishlist_count = 0

    return {'wishlist_count': wishlist_count}