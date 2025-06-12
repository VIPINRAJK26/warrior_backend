from django.contrib import admin
from warrior_app.models import MainPreview, Products, PreviewDetails,ContactSupport,HeroCarousel,User,Cart,CartItem,BuyNow,OrderItem,Invoice
# Register your models here.

admin.site.register(HeroCarousel)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(OrderItem)

class BuyNowAdmin(admin.ModelAdmin):
    search_fields = ['customer_name']
    list_display = ['user', 'customer_name', 'status']
    
admin.site.register(BuyNow, BuyNowAdmin)

class MainPreviewAdmin(admin.ModelAdmin):
    search_fields = ['category']
    
admin.site.register(MainPreview, MainPreviewAdmin)

class PreviewDetailsAdmin(admin.ModelAdmin):
    search_fields = ['category', 'subcategory', 'variant_name']
    list_display = ['category', 'subcategory', 'variant_name']
    
admin.site.register(PreviewDetails, PreviewDetailsAdmin)


class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'model_number', 'subcategory']
    list_display = ['title', 'model_number', 'price', 'subcategory']
    
admin.site.register(Products, ProductsAdmin)


class CartItemAdmin(admin.ModelAdmin):
    search_fields = ('cart', 'product')
    
admin.site.register(CartItem, CartItemAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ['order']
    list_display = ['order','invoice_number','created_at']
    
admin.site.register(Invoice, InvoiceAdmin)

@admin.register(ContactSupport)
class ContactSupportAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'support_type', 'created_at')
    list_filter = ('support_type', 'created_at')
    search_fields = ('name', 'email')