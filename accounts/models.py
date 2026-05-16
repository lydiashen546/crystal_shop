from django.db import models
from django.utils import timezone


class ShopUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=80)
    user_password = models.CharField(max_length=128)
    user_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.user_name


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name="addresses")
    recipient_name = models.CharField(max_length=80)
    phone = models.CharField(max_length=30)
    country = models.CharField(max_length=60, default="USA")
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    street = models.CharField(max_length=160)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "address"

    def __str__(self):
        return f"{self.recipient_name}, {self.city}"
