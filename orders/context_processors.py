from .cart import cart_count as count_cart


def cart_count(request):
    return {"cart_count": count_cart(request.session)}
