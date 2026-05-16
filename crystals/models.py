from django.db import models


class Crystal(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    crystal_name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    hardness = models.CharField(max_length=40, blank=True)
    origin = models.CharField(max_length=120, blank=True)
    care_instruction = models.TextField(blank=True)

    class Meta:
        db_table = "crystal"
        ordering = ["crystal_name"]

    def __str__(self):
        return self.crystal_name

    @property
    def main_image(self):
        image = self.images.filter(is_main=True).first() or self.images.first()
        if image:
            return image.image_url
        return "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?auto=format&fit=crop&w=900&q=80"


class ProductCrystal(models.Model):
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    crystal = models.ForeignKey(Crystal, on_delete=models.CASCADE)

    class Meta:
        db_table = "productcrystal"
        unique_together = ("product", "crystal")

    def __str__(self):
        return f"{self.product} - {self.crystal}"


class CrystalImage(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    crystal = models.ForeignKey(Crystal, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField()
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "crystal image"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.crystal} image {self.id}"


class CrystalEffect(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    description = models.TextField(blank=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "crystal effect"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CrystalEffectRelation(models.Model):
    crystal = models.ForeignKey(Crystal, on_delete=models.CASCADE)
    crystal_effect = models.ForeignKey(CrystalEffect, on_delete=models.CASCADE)

    class Meta:
        db_table = "crystaleffect relation"
        unique_together = ("crystal", "crystal_effect")

    def __str__(self):
        return f"{self.crystal} - {self.crystal_effect}"


class ContentSection(models.Model):
    id = models.AutoField(primary_key=True, db_column="ID")
    crystal = models.ForeignKey(Crystal, on_delete=models.CASCADE, related_name="content_sections")
    title = models.CharField(max_length=120)
    content = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "Content section"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title
