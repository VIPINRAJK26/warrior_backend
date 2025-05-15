from django.contrib import admin
from warrior_app.models import MainPreview, Products, PreviewDetails,ContactSupport,HeroCarousel,User,Cart,CartItem
# Register your models here.

admin.site.register(MainPreview)
admin.site.register(Products)
admin.site.register(PreviewDetails)
admin.site.register(HeroCarousel)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(CartItem)

@admin.register(ContactSupport)
class ContactSupportAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'support_type', 'created_at')
    list_filter = ('support_type', 'created_at')
    search_fields = ('name', 'email')