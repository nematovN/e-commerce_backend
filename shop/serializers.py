from collections import OrderedDict
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from datetime import timedelta
from .models import (
    Category, Product, Deal, Brand, Feature,
    ProductImage,  Like, Comment
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'avatar']
        read_only_fields = ['id', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])


    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'avatar']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'





class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'product']

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'text', 'created_at']
        read_only_fields = ['user', 'product', 'created_at']



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'product' ]
        read_only_fields = ['user', 'product']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)  # Mahsulotga yozilgan sharhlar
    class Meta:
        model = Product
        fields = [
            "id", "name", "description", "price", "stock", "created_at",
            "updated_at", "category", "category_name", "brand", "images",
            "features", "likes_count", "comments",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return OrderedDict(sorted(data.items()))

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class DealSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = ["product_name", "product_image", "discount", "start_time", "end_time"]

    def get_product_image(self, obj):
        first_image = obj.product.images.first()
        if first_image:
            request = self.context.get("request")
            return request.build_absolute_uri(first_image.image.url) if request else first_image.image.url
        return None

    def get_end_time(self, obj):
        if obj.end_time:
            return obj.end_time.isoformat()  # 🔥 `isoformat()` faqat datetime qiymat uchun ishlaydi
        return None  # Agar `end_time` `None` bo‘lsa, `None` qaytariladi
