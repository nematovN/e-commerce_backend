from django.contrib import admin
from .models import Category, Product, Deal, Brand,Feature
from django.contrib import admin
from .models import Product, ProductImage, User


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    exclude = ('likes',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Feature)
admin.site.register(User)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "discount", "is_active", "start_time", "end_time")


