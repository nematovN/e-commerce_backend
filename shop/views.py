from rest_framework import pagination, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.parsers import MultiPartParser, FormParser
from .models import (
    Category, Product, Brand, Feature, ProductImage, CategoryAttribute,
    ProductAttributeValue, Deal, User
)
from .serializers import (
    CategorySerializer, ProductSerializer, DealSerializer, FeatureSerializer,
    BrandSerializer, ProductImageSerializer, CategoryAttributeSerializer,
    ProductAttributeValueSerializer, UserSerializer, RegisterSerializer, LoginSerializer
)


class RegisterAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        summary="User Registration",
        description="Register user",
        request=RegisterSerializer,
        responses={
            201: OpenApiParameter(name="Tokens", description="JWT access token and refresh tokens"),
            400: OpenApiParameter(name="Errors", description="Invalid credentials")
        },
        tags=["User Authentication"]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"refresh": str(refresh), "access": access_token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        summary="User Login",
        description="Login user with email and password",
        request=LoginSerializer,
        responses={
            200: OpenApiParameter(name="Tokens", type=str, location=OpenApiParameter.QUERY,
                                 description="JWT access token and refresh tokens"),
            400: OpenApiParameter(name="Errors", type=str, location=OpenApiParameter.QUERY,
                                 description="Invalid credentials")
        },
        tags=["User Authentication"]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=user_email)
                if check_password(password, user.password):
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    return Response({"refresh": str(refresh), "access": access_token}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                pass
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProductPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryAttributeListCreateView(generics.ListCreateAPIView):
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer


class CategoryAttributeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer


class FeatureListCreateView(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class BrandListCreateView(generics.ListCreateAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        return Brand.objects.filter(category_id=category_id) if category_id else Brand.objects.all()


class BrandRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAttributeValueListCreateView(generics.ListCreateAPIView):
    queryset = ProductAttributeValue.objects.prefetch_related("attribute_values__attribute")
    serializer_class = ProductAttributeValueSerializer


class ProductAttributeValueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttributeValue.objects.prefetch_related("attribute_values__attribute")
    serializer_class = ProductAttributeValueSerializer


class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductImageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class DealListView(generics.ListAPIView):
    queryset = Deal.objects.select_related("product")
    serializer_class = DealSerializer
