from django.contrib import admin
from warrior_app.models import *
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


@admin.register(WarrentyRegistration)
class WarrentyRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'district', 'state', 'pin_code', 'product_type', 'serial_number', 'model_number', 'purchase_date', 'dealer', 'created_at')
    list_filter = ('product_type', 'purchase_date')
    search_fields = ('name', 'email', 'phone', 'address', 'district', 'state', 'pin_code', 'product_type', 'serial_number', 'model_number', 'dealer')


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


@admin.register(ModelNumberAndWarrenty)
class ModelNumberAndWarrentyAdmin(admin.ModelAdmin):
    list_display = ('model_number', 'warrenty', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('model_number', 'warrenty')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product_type',)


@admin.register(StateSelection)
class StateSelectionAdmin(admin.ModelAdmin):
    list_display = ('state', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('state',)


@admin.register(DistrictSelection)
class DistrictSelectionAdmin(admin.ModelAdmin):
    list_display = ('district', 'state', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('district', 'state')