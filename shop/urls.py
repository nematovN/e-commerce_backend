from django.urls import path

from .views import (
    # Authentication
    RegisterAPIView, LoginAPIView, UserDetailView,

    # Category
    CategoryListView, CategoryDetailView,

    # Feature
    FeatureListView, FeatureDetailView,

    # Brand
    BrandListView, BrandDetailView,

    # Product
    ProductListView, ProductDetailView, ProductImageListView,

    # Deal
    DealListView,

    # Comment
    CommentListView, CommentCreateView, CommentDeleteView,

    # Like
    add_like,  delete_like, get_comments
)

app_name = "ecommerce"

urlpatterns = [
    # =========================
    # AUTHENTICATION
    # =========================
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),

    # =========================
    # CATEGORY
    # =========================
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    # =========================
    # FEATURE
    # =========================
    path('features/', FeatureListView.as_view(), name='feature_list'),
    path('features/<int:pk>/', FeatureDetailView.as_view(), name='feature_detail'),

    # =========================
    # BRAND
    # =========================
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),

    # =========================
    # PRODUCT
    # =========================
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # =========================
    # DEAL
    # =========================
    path('deals/', DealListView.as_view(), name='deal_list'),

    # =========================
    # COMMENT
    # =========================
    path('api/products/<int:product_id>/comments/', get_comments, name='add-comment'),
    path('products/<int:product_id>/comments/add/', CommentCreateView.as_view(), name='comment-add'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # =========================
    # LIKE
    # =========================
    path('api/products/<int:product_id>/like/add/', add_like, name='add_like'),
    path('api/products/<int:product_id>/like/delete/', delete_like, name='delete_like'),

]
