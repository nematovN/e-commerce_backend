from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .managers import UserManager
from django.utils.timezone import now


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('USER', 'User')
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/student", null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name




class Feature(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.value}"


class Brand(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    features = models.ManyToManyField(Feature, related_name="products")
    likes_count = models.PositiveIntegerField(default=0)  # Like'lar soni
    likes = models.ManyToManyField(User, related_name="liked_products", blank=True)



    def __str__(self):
        return self.name

    def likes_count(self):
        return self.product_likes.count()


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attribute_values")

    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Deal(models.Model):
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    discount = models.FloatField()
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True, default=None)  # 🔥 `default=None` qo‘shildi
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Agar end_time o'tib ketgan bo'lsa, is_active ni o'chirish
        if self.end_time < now():
            self.is_active = False
        super().save(*args, **kwargs)
#   Comment

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Komment yozgan user
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')  # Qaysi productga yozilganini aniqlash uchun
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# Like

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'user')

