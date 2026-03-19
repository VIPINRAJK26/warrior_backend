from .views import *
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'contact', ContactViewSet)
router.register(r'warranty',Warranty)


urlpatterns = [
    path('api/', include(router.urls)),
    
    path('orders/',OrdersView.as_view(), name = 'dashboard-orders'),
    path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('export-data/', export_dashboard_data, name='export-data'),

]