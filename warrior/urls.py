"""
URL configuration for warrior project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from warrior_app.views import *

router = DefaultRouter()

router.register('main_preview', MainPreviewView, basename='main_preview')
router.register('products', ProductsView, basename='products')
router.register('preview_details', PreviewDetailsView, basename='preview_details')
router.register('hero_carousel', HeroCarouselView, basename='hero_carousel')
router.register('contact_support', ContactSupportViewSet, basename='contact_support')
# router.register('cart', CartViewSet, basename='cart')
# router.register('cart_item', CartItemViewSet, basename='cart_item')
router.register('buy_now', OrderViewSet, basename='buy_now')
router.register('user_orders', UserOrdersViewset, basename='user_orders')

router.register('dealer', DealerViewset, basename='dealer')
router.register('model_number_and_warrenty', ModelNumberAndWarrentyViewset, basename='model_number_and_warrenty')
router.register('product_type', ProductTypeViewset, basename='product_type')
router.register('states', StateSelectionViewset, basename='states')
router.register('districts', DistrictSelectionViewset, basename='districts')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart_item/', CartItemView.as_view(), name='cart_item'),
    path("api/cart_item/<int:pk>/", CartItemView.as_view()),
    path("api/cart/clear/", ClearCartView.as_view()),
    path("api/cart/merge/", CartMergeView.as_view()),
    path('api/filters/<str:subcategory_slug>/', FilterOptionsView.as_view() , name='filter_options'),
    path('api/create-razorpay-order/', create_razorpay_order),
    path('api/brochures/<str:filename>', brochure_view, name='brochure_view'),
    path("api/warrenty_registration/", warrenty_registration),
    

    path('dashboard/',include('Dashboard.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
