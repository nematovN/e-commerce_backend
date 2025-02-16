from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import (
    Category, Product, Brand, Feature, ProductImage,
    CategoryAttribute, ProductAttributeValue, Deal
)
from .serializers import (
    CategorySerializer, ProductSerializer,
    DealSerializer, FeatureSerializer, BrandSerializer, ProductImageSerializer,
    CategoryAttributeSerializer, ProductAttributeValueSerializer
)


from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Oddiy user ro'yxatdan o'tishi uchun"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """Login qilgandan keyin userni tegishli sahifaga yo'naltirish"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({
                "message": "Login successful",
                "redirect_url": user.get_redirect_url()  # Yo‘naltirish URL'si
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """Foydalanuvchi profilini ko'rish va tahrirlash"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Pagination class
class ProductPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Category API
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Category Attribute API
class CategoryAttributeListCreateView(generics.ListCreateAPIView):
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer

class CategoryAttributeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer

# Feature API
class FeatureListCreateView(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

# Brand API (faqat tegishli category bo‘yicha filter qilinadi)
class BrandListCreateView(generics.ListCreateAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Brand.objects.filter(category_id=category_id)
        return Brand.objects.all()

class BrandRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Product API
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Product Attribute Value API
class ProductAttributeValueListCreateView(generics.ListCreateAPIView):
    queryset = ProductAttributeValue.objects.prefetch_related("attribute_values__attribute")
    serializer_class = ProductAttributeValueSerializer

class ProductAttributeValueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttributeValue.objects.prefetch_related("attribute_values__attribute")
    serializer_class = ProductAttributeValueSerializer

# Product Image API
class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ProductImageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


# Deal API (faqat o‘qish uchun)
class DealListView(generics.ListAPIView):
    queryset = Deal.objects.select_related("product")
    serializer_class = DealSerializer

@swagger_auto_schema(method="get", responses={200: DealSerializer(many=True)})
@api_view(["GET"])
def deal_list(request):
    deals = Deal.objects.select_related("product")
    serializer = DealSerializer(deals, many=True)
    return Response(serializer.data)
