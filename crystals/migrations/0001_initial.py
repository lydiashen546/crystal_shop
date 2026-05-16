from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Crystal",
            fields=[
                ("id", models.AutoField(db_column="ID", primary_key=True, serialize=False)),
                ("crystal_name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("hardness", models.CharField(blank=True, max_length=40)),
                ("origin", models.CharField(blank=True, max_length=120)),
                ("care_instruction", models.TextField(blank=True)),
            ],
            options={"db_table": "crystal", "ordering": ["crystal_name"]},
        ),
        migrations.CreateModel(
            name="CrystalEffect",
            fields=[
                ("id", models.AutoField(db_column="ID", primary_key=True, serialize=False)),
                ("description", models.TextField(blank=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={"db_table": "crystal effect", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="ContentSection",
            fields=[
                ("id", models.AutoField(db_column="ID", primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=120)),
                ("content", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("crystal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="content_sections", to="crystals.crystal")),
            ],
            options={"db_table": "Content section", "ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="CrystalEffectRelation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("crystal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="crystals.crystal")),
                ("crystal_effect", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="crystals.crystaleffect")),
            ],
            options={"db_table": "crystaleffect relation", "unique_together": {("crystal", "crystal_effect")}},
        ),
        migrations.CreateModel(
            name="CrystalImage",
            fields=[
                ("id", models.AutoField(db_column="ID", primary_key=True, serialize=False)),
                ("image_url", models.URLField()),
                ("is_main", models.BooleanField(default=False)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("crystal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="crystals.crystal")),
            ],
            options={"db_table": "crystal image", "ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="ProductCrystal",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("crystal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="crystals.crystal")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="catalog.product")),
            ],
            options={"db_table": "productcrystal", "unique_together": {("product", "crystal")}},
        ),
    ]
