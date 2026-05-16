from django.db import models
from django.utils import timezone


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("accounts.ShopUser", on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE, related_name="reviews")
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, related_name="reviews", null=True, blank=True)
    comment = models.TextField()
    rate = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "review"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product} review {self.rate}/5"
