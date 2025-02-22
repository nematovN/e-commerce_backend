from django.contrib import admin
from .models import Category, Product, Deal, Brand,Feature
from django.contrib import admin
from .models import Product, ProductImage, User


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Feature)
admin.site.register(User)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'start_time', 'end_time')
    search_fields = ('product__name',)







