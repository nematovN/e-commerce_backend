from django.contrib import admin
from .models import Category, Product, Deal, Brand,Feature ,ProductAttributeValue
from django.contrib import admin
from .models import Product, ProductImage,CategoryAttribute


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # 3ta rasm yuklash imkoniyati

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Feature)
admin.site.register(ProductAttributeValue)
admin.site.register(CategoryAttribute)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'start_time', 'end_time')
    search_fields = ('product__name',)







