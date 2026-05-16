from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Address, ShopUser
from catalog.models import Category, Product, ProductImage
from crystals.models import ContentSection, Crystal, CrystalEffect, CrystalEffectRelation, CrystalImage, ProductCrystal
from orders.models import Order, OrderItem
from reviews.models import Review


class Command(BaseCommand):
    help = "Create sample data for the crystal shopping platform."

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING("Seed data already exists."))
            return

        jewelry = Category.objects.create(category="Crystal Jewelry")
        decor = Category.objects.create(category="Home Decor")
        healing = Category.objects.create(category="Healing Sets")

        amethyst = Crystal.objects.create(
            crystal_name="Amethyst",
            description="Purple quartz loved for calm, clarity, and elegant color.",
            hardness="7 Mohs",
            origin="Brazil",
            care_instruction="Avoid long direct sunlight; clean with a soft dry cloth.",
        )
        rose = Crystal.objects.create(
            crystal_name="Rose Quartz",
            description="Soft pink quartz associated with warmth and self-care.",
            hardness="7 Mohs",
            origin="Madagascar",
            care_instruction="Rinse briefly with lukewarm water and dry immediately.",
        )
        clear = Crystal.objects.create(
            crystal_name="Clear Quartz",
            description="Transparent quartz often used as a versatile display crystal.",
            hardness="7 Mohs",
            origin="Arkansas",
            care_instruction="Keep away from abrasive surfaces to preserve polish.",
        )

        calm = CrystalEffect.objects.create(name="Calming", description="Creates a quiet, relaxed atmosphere.")
        love = CrystalEffect.objects.create(name="Love", description="Often selected for heartfelt gifts.")
        focus = CrystalEffect.objects.create(name="Focus", description="Popular on desks and study spaces.")

        for crystal, effect in [(amethyst, calm), (rose, love), (clear, focus), (clear, calm)]:
            CrystalEffectRelation.objects.create(crystal=crystal, crystal_effect=effect)

        ContentSection.objects.create(crystal=amethyst, title="Best Placement", content="Place near a bedside table or reading corner.", sort_order=1)
        ContentSection.objects.create(crystal=rose, title="Gift Note", content="Pairs well with soft gold jewelry and handwritten cards.", sort_order=1)
        ContentSection.objects.create(crystal=clear, title="Care Tip", content="Store separately from softer stones.", sort_order=1)

        products = [
            Product.objects.create(
                category=jewelry,
                product_name="Amethyst Pendant",
                price=Decimal("39.00"),
                stock_quantity=18,
                description="A polished amethyst pendant on a silver-tone chain.",
            ),
            Product.objects.create(
                category=decor,
                product_name="Rose Quartz Heart",
                price=Decimal("28.50"),
                stock_quantity=24,
                description="Hand-carved rose quartz heart for gifting or decor.",
            ),
            Product.objects.create(
                category=healing,
                product_name="Clear Quartz Focus Set",
                price=Decimal("52.00"),
                stock_quantity=12,
                description="Three clear quartz points arranged as a desk focus set.",
            ),
        ]

        for product, crystal in [(products[0], amethyst), (products[1], rose), (products[2], clear)]:
            ProductCrystal.objects.create(product=product, crystal=crystal)

        product_images = [
            "https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?auto=format&fit=crop&w=900&q=80",
        ]
        for product, image_url in zip(products, product_images):
            ProductImage.objects.create(product=product, image_url=image_url, is_main=True)

        crystal_images = {
            amethyst: "https://images.unsplash.com/photo-1617791160505-6f00504e3519?auto=format&fit=crop&w=900&q=80",
            rose: "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=900&q=80",
            clear: "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?auto=format&fit=crop&w=900&q=80",
        }
        for crystal, image_url in crystal_images.items():
            CrystalImage.objects.create(crystal=crystal, image_url=image_url, is_main=True)

        demo_user = ShopUser.objects.create(
            user_name="demo_customer",
            user_password="demo123",
            user_email="demo@example.com",
            phone="312-555-0199",
        )
        address = Address.objects.create(
            user=demo_user,
            recipient_name="Demo Customer",
            phone="312-555-0199",
            country="USA",
            state="IL",
            city="Chicago",
            street="100 Crystal Lane",
            postal_code="60601",
            is_default=True,
        )
        order = Order.objects.create(
            total_amount=products[0].price,
            status="paid",
            payment_method="card",
            paid_at=timezone.now(),
            user=demo_user,
            address=address,
        )
        OrderItem.objects.create(order=order, product=products[0], quantity=1)
        Review.objects.create(user=demo_user, product=products[0], order=order, rate=5, comment="Beautiful color and fast shipping.")

        self.stdout.write(self.style.SUCCESS("Seed data created."))
