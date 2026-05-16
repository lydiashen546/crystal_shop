from django.db.models import Avg
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from crystals.models import ContentSection, ProductCrystal
from reviews.models import Review

from .models import Category, Product


def index(request):
    category_id = request.GET.get("category")
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")
    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = products.filter(
            Q(product_name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__category__icontains=query)
        )
    categories = Category.objects.all()
    return render(
        request,
        "catalog/index.html",
        {"products": products, "categories": categories, "query": query, "selected_category": category_id},
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images"),
        pk=product_id,
        is_active=True,
    )
    crystal_ids = ProductCrystal.objects.filter(product=product).values_list("crystal_id", flat=True)
    crystals = ProductCrystal.objects.filter(product=product).select_related("crystal")
    crystal_profiles = [
        {
            "crystal": product_crystal.crystal,
            "sections": ContentSection.objects.filter(crystal=product_crystal.crystal),
        }
        for product_crystal in crystals
    ]
    reviews = Review.objects.filter(product=product).select_related("user")
    avg_rating = reviews.aggregate(value=Avg("rate"))["value"]
    product_images = list(product.images.all())
    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
            "crystal_ids": crystal_ids,
            "crystal_profiles": crystal_profiles,
            "reviews": reviews,
            "avg_rating": avg_rating,
            "product_images": product_images,
        },
    )
