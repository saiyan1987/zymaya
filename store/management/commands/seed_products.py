from django.core.management.base import BaseCommand
from django.utils.text import slugify

from store.models import Category, Product, ProductVariant


class Command(BaseCommand):
    help = "Seed demo Zymaya products"

    def handle(self, *args, **kwargs):
        categories = {
            "Bags": Category.objects.get_or_create(
                name="Bags",
                slug="bags",
                defaults={"image_label": "Bags"},
            )[0],
            "Shoes": Category.objects.get_or_create(
                name="Shoes",
                slug="shoes",
                defaults={"image_label": "Shoes"},
            )[0],
            "Slippers": Category.objects.get_or_create(
                name="Slippers",
                slug="slippers",
                defaults={"image_label": "Slippers"},
            )[0],
            "Clothing": Category.objects.get_or_create(
                name="Clothing",
                slug="clothing",
                defaults={"image_label": "Clothing"},
            )[0],
        }

        products = [
            {
                "name": "Zymaya Quilted Chain Bag",
                "category": "Bags",
                "brand": "Zymaya",
                "price": 249.99,
                "colour": "Black",
                "image": "products/quilted-chain-bag.jpg",
                "sizes": ["One Size"],
                "stock": 4,
            },
            {
                "name": "Zymaya Mini Tote Bag",
                "category": "Bags",
                "brand": "Zymaya",
                "price": 189.99,
                "colour": "Cream",
                "image": "products/mini-tote-bag.jpg",
                "sizes": ["One Size"],
                "stock": 3,
            },
            {
                "name": "Zymaya Luxe Mule Slippers",
                "category": "Slippers",
                "brand": "Zymaya",
                "price": 89.99,
                "colour": "Taupe",
                "image": "products/luxe-mule-slippers.jpg",
                "sizes": ["UK 4", "UK 5", "UK 6", "UK 7"],
                "stock": 5,
            },
            {
                "name": "Zymaya Satin Evening Heels",
                "category": "Shoes",
                "brand": "Zymaya",
                "price": 129.99,
                "colour": "Black",
                "image": "products/satin-evening-heels.jpg",
                "sizes": ["UK 4", "UK 5", "UK 6", "UK 7", "UK 8"],
                "stock": 2,
            },
            {
                "name": "Zymaya Signature Trainers",
                "category": "Shoes",
                "brand": "Zymaya",
                "price": 149.99,
                "colour": "White",
                "image": "products/signature-trainers.jpg",
                "sizes": ["UK 5", "UK 6", "UK 7", "UK 8"],
                "stock": 3,
            },
            {
                "name": "Zymaya Velvet Co-ord Set",
                "category": "Clothing",
                "brand": "Zymaya",
                "price": 119.99,
                "colour": "Chocolate",
                "image": "products/velvet-coord-set.jpg",
                "sizes": ["S", "M", "L", "XL"],
                "stock": 4,
            },
        ]

        for item in products:
            product, created = Product.objects.get_or_create(
                slug=slugify(item["name"]),
                defaults={
                    "name": item["name"],
                    "category": categories[item["category"]],
                    "brand": item["brand"],
                    "base_price": item["price"],
                    "colour": item["colour"],
                    "image": item["image"],
                    "description": f"A luxury {item['category'].lower()} piece from Zymaya.",
                    "is_featured": True,
                    "is_active": True,
                },
            )

            for size in item["sizes"]:
                ProductVariant.objects.get_or_create(
                    product=product,
                    size=size,
                    defaults={
                        "stock": item["stock"],
                        "price": item["price"],
                        "sku": f"{slugify(item['name']).upper()}-{size.replace(' ', '').upper()}",
                    },
                )

        self.stdout.write(self.style.SUCCESS("Demo Zymaya products created successfully."))