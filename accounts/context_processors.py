from .auth import get_current_user


def current_shop_user(request):
    return {"current_shop_user": get_current_user(request)}
