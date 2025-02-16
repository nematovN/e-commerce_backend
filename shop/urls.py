from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    FeatureListCreateView, FeatureRetrieveUpdateDestroyView,
    BrandListCreateView, BrandRetrieveUpdateDestroyView,
    CategoryAttributeListCreateView, CategoryAttributeRetrieveUpdateDestroyView,
    ProductAttributeValueListCreateView, ProductAttributeValueRetrieveUpdateDestroyView,
    ProductImageListCreateView, DealListView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Category URLs
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    # Product URLs
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),



    # Feature URLs
    path('api/features/', FeatureListCreateView.as_view(), name='feature-list-create'),
    path('api/features/<int:pk>/', FeatureRetrieveUpdateDestroyView.as_view(), name='feature-detail'),

    # Brand URLs
    path('api/brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('api/brands/<int:pk>/', BrandRetrieveUpdateDestroyView.as_view(), name='brand-detail'),

    # Category Attribute URLs
    path('api/category-attributes/', CategoryAttributeListCreateView.as_view(), name='category-attribute-list-create'),
    path('api/category-attributes/<int:pk>/', CategoryAttributeRetrieveUpdateDestroyView.as_view(),
         name='category-attribute-detail'),

    # Product Attribute Value URLs
    path('api/product-attribute-values/', ProductAttributeValueListCreateView.as_view(),
         name='product-attribute-value-list-create'),
    path('api/product-attribute-values/<int:pk>/', ProductAttributeValueRetrieveUpdateDestroyView.as_view(),
         name='product-attribute-value-detail'),

    # Other Endpoints
    path('api/products-list/', ProductListCreateView.as_view(), name='product-list'),
    path('api/deals/', DealListView.as_view(), name='deal-list'),

    # Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
