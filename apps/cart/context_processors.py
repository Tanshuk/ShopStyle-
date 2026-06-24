"""
Cart context processor — safe version with full exception handling.
"""


def cart_context(request):
    """
    Inject cart_count into every template.
    Returns 0 safely if anything goes wrong.
    """
    cart_count = 0

    try:
        session_cart = request.session.get('cart', {})
        if isinstance(session_cart, dict):
            cart_count = sum(
                v if isinstance(v, int) else v.get('quantity', 1)
                for v in session_cart.values()
            )
    except Exception:
        cart_count = 0

    return {'cart_count': cart_count}