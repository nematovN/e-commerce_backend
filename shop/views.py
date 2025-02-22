from django.contrib.auth.hashers import make_password, check_password
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView

from .models import Category, Product, Brand, Feature, ProductImage, Deal, User, Like, Comment
from .serializers import (
    CategorySerializer, ProductSerializer, DealSerializer, FeatureSerializer,
    BrandSerializer, ProductImageSerializer, UserSerializer, RegisterSerializer,
    LoginSerializer, CommentSerializer, LikeSerializer
)


# ==========================
# AUTH API (Register & Login)
# ==========================

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(summary="User Registration", description="Register a new user", request=RegisterSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(summary="User Login", description="Login user with email and password", request=LoginSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                if check_password(serializer.validated_data['password'], user.password):
                    refresh = RefreshToken.for_user(user)
                    return Response({"refresh": str(refresh), "access": str(refresh.access_token)},
                                    status=status.HTTP_200_OK)
            except User.DoesNotExist:
                pass
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# =====================
# CATEGORY API
# =====================

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# =====================
# PRODUCT API
# =====================

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    pagination_class =   None


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# =====================
# PRODUCT IMAGE API
# =====================

class ProductImageListView(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


# =====================
# DEAL API
# =====================

class DealListView(generics.ListAPIView):
    queryset = Deal.objects.select_related("product")
    serializer_class = DealSerializer


# =====================
# FEATURE API
# =====================

class FeatureListView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureDetailView(generics.RetrieveAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


# =====================
# BRAND API
# =====================

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# =====================
# COMMENT VIEWS
# =====================

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        return Comment.objects.filter(product_id=product_id)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        serializer.save(user=self.request.user, product=product)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'detail': 'You can only delete your own comment!'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({'detail': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)


# =====================
# LIKE VIEWS
# =====================

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        if Like.objects.filter(user=self.request.user, product=product).exists():
            return Response({'detail': 'You have already liked this product!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user, product=product)


class LikeDeleteView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        like = Like.objects.filter(user=request.user, product_id=product_id).first()
        if like:
            like.delete()
            return Response({'detail': 'Like removed'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)
