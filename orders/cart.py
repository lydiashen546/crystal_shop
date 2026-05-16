from decimal import Decimal

from catalog.models import Product


def get_cart(session):
    return session.setdefault("cart", {})


def cart_count(session):
    return sum(int(qty) for qty in get_cart(session).values())


def cart_lines(session):
    data = get_cart(session)
    product_ids = [int(pid) for pid in data.keys()]
    products = Product.objects.filter(product_id__in=product_ids)
    lines = []
    total = Decimal("0.00")
    for product in products:
        quantity = int(data.get(str(product.product_id), 0))
        line_total = product.price * quantity
        total += line_total
        lines.append({"product": product, "quantity": quantity, "line_total": line_total})
    return lines, total
