from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "Create sample products for caching experiments"

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write("Products already exist.")
            return

        products = [
            Product(
                name=f"Product {i}",
                description=f"Description for product {i}",
                price=100 + i,
                stock=50 + i,
            )
            for i in range(1, 1001)
        ]

        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS("Created 1000 products."))
