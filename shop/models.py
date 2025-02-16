from django.utils import timezone
from datetime import timedelta
from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="attributes")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Feature(models.Model):
    name = models.CharField(max_length=255)  # Masalan, "Color", "Storage"
    value = models.CharField(max_length=255)  # Masalan, "Red", "128GB"

    def __str__(self):
        return f"{self.name}: {self.value}"

class Brand(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return self.name

# Product


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    features = models.ManyToManyField(Feature, related_name="products")
    def __str__(self):
        return self.name

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attribute_values")
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)




class Deal(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='deals')
    product_name = models.CharField(max_length=255, help_text='Enter product name')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Chegirma foizda (%)")
    start_time = models.DateTimeField(default=timezone.now, help_text="Chegirma boshlanish vaqti")
    duration = models.DurationField(default=timedelta(hours=24), help_text="Chegirma qancha davom etadi (masalan, 24 soat)")
    end_time = models.DateTimeField(null=True, blank=True, help_text="Chegirma tugash vaqti")
    is_active = models.BooleanField(default=True, help_text="Chegirma aktiv yoki yo'q")

    def save(self, *args, **kwargs):
        """Chegirma tugash vaqtini avtomatik hisoblaydi"""
        self.end_time = self.start_time + self.duration
        super().save(*args, **kwargs)

    def is_valid(self):
        """Chegirma hali tugamaganligini tekshiradi"""
        return self.start_time <= timezone.now() <= self.end_time

    def __str__(self):
        return f"{self.product.name} - {self.discount_percent}% chegirma ({self.duration})"


