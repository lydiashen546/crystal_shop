from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.auth import get_current_user
from accounts.models import Address, ShopUser
from catalog.models import Product

from .cart import cart_lines, get_cart
from .models import Order, OrderItem


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    data = get_cart(request.session)
    key = str(product.product_id)
    data[key] = min(product.stock_quantity, int(data.get(key, 0)) + quantity)
    request.session.modified = True
    messages.success(request, f"{product.product_name} added to cart.")
    return redirect("cart")


def cart_view(request):
    lines, total = cart_lines(request.session)
    return render(request, "orders/cart.html", {"lines": lines, "total": total})


@require_POST
def remove_from_cart(request, product_id):
    data = get_cart(request.session)
    data.pop(str(product_id), None)
    request.session.modified = True
    return redirect("cart")


def checkout(request):
    data = get_cart(request.session)
    if not data:
        return redirect("cart")

    lines, total = cart_lines(request.session)
    products = [line["product"] for line in lines]

    if request.method == "POST":
        user = get_current_user(request)
        is_guest_checkout = user is None
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        full_name = f"{first_name} {last_name}".strip()
        if not user:
            email = request.POST["user_email"].strip().lower()
            user, _ = ShopUser.objects.get_or_create(
                user_email=email,
                defaults={
                    "user_name": full_name,
                    "user_password": "checkout-created",
                    "phone": request.POST["phone"].strip(),
                },
            )
        address = Address.objects.create(
            user=user,
            recipient_name=full_name,
            phone=request.POST["phone"].strip(),
            country=request.POST["country"].strip(),
            state=request.POST["state"].strip(),
            city=request.POST["city"].strip(),
            street=request.POST["street"].strip(),
            postal_code=request.POST["postal_code"].strip(),
            is_default=False,
        )
        order = Order.objects.create(
            total_amount=total,
            status="paid",
            payment_method=request.POST["payment_method"],
            paid_at=timezone.now(),
            user=user,
            address=address,
        )
        for product in products:
            quantity = int(data[str(product.product_id)])
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            product.stock_quantity = max(0, product.stock_quantity - quantity)
            product.save(update_fields=["stock_quantity", "updated_at"])
        request.session["cart"] = {}
        if is_guest_checkout:
            messages.success(request, "Your order was placed. Login is required to view order history.")
            return redirect("index")
        return redirect("order_detail", order_id=order.order_id)

    current_user = get_current_user(request)
    name_parts = (current_user.user_name.split(" ", 1) if current_user else ["Guest", "Customer"])
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    return render(
        request,
        "orders/checkout.html",
        {"total": total, "checkout_first_name": first_name, "checkout_last_name": last_name},
    )


def orders(request):
    user = get_current_user(request)
    if not user:
        messages.info(request, "Please login to view your orders.")
        return redirect("login")
    order_list = Order.objects.filter(user=user).select_related("user", "address").prefetch_related("items")
    return render(request, "orders/list.html", {"orders": order_list})


def order_detail(request, order_id):
    user = get_current_user(request)
    if not user:
        messages.info(request, "Please login to view your order.")
        return redirect("login")
    order = get_object_or_404(Order.objects.select_related("user", "address"), pk=order_id, user=user)
    items = OrderItem.objects.filter(order=order).select_related("product")
    return render(request, "orders/detail.html", {"order": order, "items": items})
