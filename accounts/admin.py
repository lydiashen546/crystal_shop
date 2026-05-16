from django.contrib import admin

from .models import Address, ShopUser


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user_name", "user_email", "phone", "is_active", "created_at")
    search_fields = ("user_name", "user_email", "phone")
    list_filter = ("is_active",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address_id", "recipient_name", "city", "state", "country", "is_default")
    search_fields = ("recipient_name", "phone", "city", "street")
