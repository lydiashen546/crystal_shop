from django.db import models
from django.utils import timezone


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=80, unique=True)

    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    product_name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "product"
        ordering = ["product_name"]

    def __str__(self):
        return self.product_name

    @property
    def main_image(self):
        image = self.images.filter(is_main=True).first() or self.images.first()
        if image:
            return image.image_url
        return "https://images.unsplash.com/photo-1617791160505-6f00504e3519?auto=format&fit=crop&w=900&q=80"


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField()
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "product image"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product} image {self.id}"
