from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import now
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import User, Category, Product, ProductImage, Deal, Feature, Brand, Comment, Like
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, CategorySerializer,
    ProductSerializer, ProductImageSerializer, DealSerializer, FeatureSerializer,
    BrandSerializer, CommentSerializer
)

444

# =====================
# AUTH API
# =====================


@extend_schema_view(
    post=extend_schema(
        summary="User Registration",
        description="Register a new user and get access & refresh tokens.",
        request=RegisterSerializer,
        tags=["User Authentication API"]  # 🔥 Auth API tagi
    )
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):                                                                                                          # noqa
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        summary="User Login",
        description="Login user with email and password and get access & refresh tokens.",
        request=LoginSerializer,
        tags=["User Authentication API"]
    )
)
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    parser_classes = (MultiPartParser, FormParser)

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


# =====================
# USER API
# =====================

@extend_schema_view(
    get=extend_schema(
        summary="Get User Profile",
        description="Retrieve the authenticated user's details.",
        tags=["User API"]
    )
)
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# =====================
# CATEGORY API
# =====================

@extend_schema_view(
    get=extend_schema(
        summary="List All Categories",
        description="Retrieve all product categories.",
        tags=["Category API"]
    )
)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve a Category",
        description="Get details of a specific category.",
        tags=["Category API"]
    )
)
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# =====================
# PRODUCT API
# =====================

@extend_schema_view(
    get=extend_schema(
        summary="List All Products",
        description="Retrieve all products with related comments, images, features, and likes.",
        tags=["Product API"]
    )
)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related("comments", "images", "features", "likes").all().order_by('-id')
    serializer_class = ProductSerializer


@extend_schema(
    summary="Retrieve a Product",
    description="Get details of a specific product.",
    tags=["Product API"]
)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# =====================
# PRODUCT IMAGE API
# =====================

@extend_schema(
    summary="List All Product Images",
    description="Retrieve all images associated with products.",
    tags=["Product API"]
)
class ProductImageListView(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


# =====================
# DEAL API
# =====================

@extend_schema(
    summary="List All Deals",
    description="Retrieve all discount deals with related products.",
    tags=["Discount API"]
)
class DealListView(generics.ListAPIView):
    serializer_class = DealSerializer

    def get_queryset(self):
        queryset = Deal.objects.select_related("product")

        # Avtomatik yangilash
        Deal.objects.filter(is_active=True, end_time__lt=now()).update(is_active=False)

        # Endi faqat faollari olish
        queryset = queryset.filter(is_active=True, end_time__gt=now()) | queryset.filter(is_active=True,
                                                                                         end_time__isnull=True)  # noqa

        # 🔥 Query parameter: discount filter
        discount_min = self.request.query_params.get("min_discount")
        discount_max = self.request.query_params.get("max_discount")

        if discount_min:
            queryset = queryset.filter(discount__gte=float(discount_min))
        if discount_max:
            queryset = queryset.filter(discount__lte=float(discount_max))

        return queryset


# =====================
# FEATURE API
# =====================

@extend_schema(
    summary="List All Features",
    description="Retrieve all features associated with products.",
    tags=["Feature API"]
)
class FeatureListView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


@extend_schema(
    summary="Retrieve a Feature",
    description="Get details of a specific product feature.",
    tags=["Feature API"]
)
class FeatureDetailView(generics.RetrieveAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


# =====================
# BRAND API
# =====================

@extend_schema(
    summary="List All Brands",
    description="Retrieve all available brands.",
    tags=["Brand API"]
)
class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


@extend_schema(
    summary="Retrieve a Brand",
    description="Get details of a specific brand.",
    tags=["Brand API"]
)
class BrandDetailView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# =====================
# COMMENT API
# =====================

@extend_schema(
    summary="List All Comments",
    description="Add a new comment to a product.",
    tags=["Comment API"]
)
@api_view(['GET'])
def get_comments(request, product_id):
    comments = Comment.objects.filter(product_id=product_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({"count": len(comments), "results": serializer.data})


@extend_schema(
    description="Add a new comment to a product.",
    tags=["Comment API"]
)
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        return Comment.objects.filter(product_id=product_id)


@extend_schema(
    summary="Create a Comment",
    description="Add a new comment to a product.",
    tags=["Comment API"]
)
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product)


@extend_schema(
    summary="Delete a Comment",
    description="Add a new comment to a product.",
    tags=["Comment API"]
)
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
# LIKE API
# =====================

@extend_schema(
    tags=["Like Api"],
    summary="Add Like to a Product",
    description="User likes a product. If already liked, returns an error."

)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    like, created = Like.objects.get_or_create(product=product, user=request.user)

    if created:
        return Response({"message": "Liked!", "likes_count": product.likes_count()}, status=201)

    return Response({"message": "Already liked", "likes_count": product.likes_count()}, status=400)


@extend_schema(
    tags=["Like Api"],
    summary="Add Like to a Product",
    description="User likes a product. If already liked, returns an error."

)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    like = Like.objects.filter(product=product, user=request.user)

    if like.exists():
        like.delete()
        return Response({"message": "Like removed!", "likes_count": product.likes_count()}, status=200)

    return Response({"message": "You haven't liked this product yet"}, status=400)
