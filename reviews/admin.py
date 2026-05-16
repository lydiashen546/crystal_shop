from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "product", "user", "rate", "created_at")
    list_filter = ("rate",)
    search_fields = ("comment", "product__product_name", "user__user_name")
