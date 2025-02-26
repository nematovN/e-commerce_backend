from django.test import TestCase

# Create your tests here.
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # settings faylini yuklash
django.setup()

from shop.models import Product

for product in Product.objects.all():
    print(f"ID: {product.id}, Name: {product.name}")
