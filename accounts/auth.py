from .models import ShopUser


SESSION_USER_ID = "shop_user_id"


def get_current_user(request):
    user_id = request.session.get(SESSION_USER_ID)
    if not user_id:
        return None
    try:
        return ShopUser.objects.get(pk=user_id, is_active=True)
    except ShopUser.DoesNotExist:
        request.session.pop(SESSION_USER_ID, None)
        return None


def login_user(request, user):
    request.session[SESSION_USER_ID] = user.user_id


def logout_user(request):
    request.session.pop(SESSION_USER_ID, None)
