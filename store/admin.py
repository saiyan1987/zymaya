from django.contrib import admin
from .models import Category, Product, ProductVariant, Order, OrderItem
class ProductVariantInline(admin.TabularInline):
    model=ProductVariant; extra=1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','brand','category','base_price','is_featured','is_active','total_stock')
    list_filter=('category','is_featured','is_active','brand')
    prepopulated_fields={'slug':('name',)}
    inlines=[ProductVariantInline]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    prepopulated_fields={'slug':('name',)}
class OrderItemInline(admin.TabularInline):
    model=OrderItem; extra=0; readonly_fields=('variant','quantity','price')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','full_name','email','status','total','created_at')
    list_filter=('status','created_at')
    inlines=[OrderItemInline]
