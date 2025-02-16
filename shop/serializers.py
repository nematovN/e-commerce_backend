from rest_framework import serializers
from .models import Category, Product,   Deal, Brand, Feature, ProductImage, CategoryAttribute, ProductAttributeValue
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'avatar']
        read_only_fields = ['id', 'role']  # Role ni user o'zi o'zgartira olmasligi uchun


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user





class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryAttribute
        fields = "__all__"


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ["id", "attribute", "attribute_name", "value"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product_id']

        def get_image(self, obj):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)  # To‘liq URL yaratish
            return obj.image.url  # Agar request bo‘lmasa, faqat nisbiy yo‘lni qaytarish

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "created_at", "updated_at", "category", "brand", "images", "features",'attribute_values' , 'category_name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']  # Brend haqida faqat ID va nomni qaytaramiz    # noqa
        category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')


from rest_framework import serializers
from .models import Deal, Product  # Deal va Product modellari

class DealSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = ["product_name", "product_image", "discount_percent", "start_time", "end_time"]

    def get_end_time(self, obj):
        return obj.start_time + obj.duration

