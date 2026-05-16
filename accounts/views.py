from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .auth import get_current_user, login_user, logout_user
from .models import ShopUser


def login_view(request):
    if get_current_user(request):
        return redirect("orders")

    next_url = request.GET.get("next") or request.POST.get("next") or "orders"
    if request.method == "POST":
        email = request.POST["user_email"].strip().lower()
        password = request.POST["user_password"]
        user = ShopUser.objects.filter(user_email=email, user_password=password, is_active=True).first()
        if user:
            login_user(request, user)
            messages.success(request, f"Welcome back, {user.user_name}.")
            return redirect(next_url)
        messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html", {"next": next_url})


def signup_view(request):
    if get_current_user(request):
        return redirect("orders")

    if request.method == "POST":
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        email = request.POST["user_email"].strip().lower()
        password = request.POST["user_password"]
        phone = request.POST["phone"].strip()
        full_name = f"{first_name} {last_name}".strip()

        user = ShopUser.objects.filter(user_email=email).first()
        if user and user.user_password != "checkout-created":
            messages.error(request, "An account with this email already exists. Please login.")
            return render(request, "accounts/signup.html")

        if user:
            user.user_name = full_name
            user.user_password = password
            user.phone = phone
            user.is_active = True
            user.save(update_fields=["user_name", "user_password", "phone", "is_active", "updated_at"])
        else:
            user = ShopUser.objects.create(
                user_name=full_name,
                user_password=password,
                user_email=email,
                phone=phone,
            )

        login_user(request, user)
        messages.success(request, f"Welcome, {user.user_name}.")
        return redirect("orders")

    return render(request, "accounts/signup.html")


@require_POST
def logout_view(request):
    logout_user(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")
