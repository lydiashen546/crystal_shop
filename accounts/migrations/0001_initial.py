from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShopUser",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("user_name", models.CharField(max_length=80)),
                ("user_password", models.CharField(max_length=128)),
                ("user_email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"db_table": "user"},
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                ("address_id", models.AutoField(primary_key=True, serialize=False)),
                ("recipient_name", models.CharField(max_length=80)),
                ("phone", models.CharField(max_length=30)),
                ("country", models.CharField(default="USA", max_length=60)),
                ("state", models.CharField(max_length=60)),
                ("city", models.CharField(max_length=60)),
                ("street", models.CharField(max_length=160)),
                ("postal_code", models.CharField(max_length=20)),
                ("is_default", models.BooleanField(default=False)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="addresses", to="accounts.shopuser")),
            ],
            options={"db_table": "address"},
        ),
    ]
