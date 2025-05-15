from rest_framework import viewsets
from .serializers import MainPreviewSerializer, ProductsSerializer, PreviewDetailsSerializer, HeroCarouselSerializer,ContactSupportSerializer,LoginSerializer,RegisterSerializer,CartItemSerializer,CartSerializer,BuyNowSerializer,OrderItemSerializer
from .models import MainPreview, Products, PreviewDetails,HeroCarousel,ContactSupport,Cart,CartItem,BuyNow,OrderItem
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import serializers
import logging
from decimal import Decimal


logger = logging.getLogger(__name__)


# Create your views here.


class MainPreviewView(viewsets.ModelViewSet):
    queryset = MainPreview.objects.all()
    serializer_class = MainPreviewSerializer
    
# CATEGORY_FILTERS = {
#     'home_ups': ['variant', 'va_rating', 'voltage', 'warranty', 'price'],
#     'solar_power': ['variant', 'sku', 'input_voltage_range', 'output_power'],
#     'batteries': ['variant', 'sku', 'price', 'weight', 'voltage'],
# }

SUB_CATEGORY_FILTERS = {
    "online_ups": ['variant', 'va_rating', 'voltage_min', 'warranty', 'price'],
    "offline_ups": ['variant', 'va_rating', 'voltage_min', 'warranty', 'price'],
    "hkva_ups": ['variant', 'va_rating', 'voltage_min', 'warranty', 'price'],
    "solar_ups": ['variant', 'va_rating', 'voltage_min', 'warranty', 'price'],
    "solar_panel": ['product_series', 'voltage_min', 'wattage', 'price'],
    "lithium_solar_inverter": ['variant', 'va_rating', 'voltage_min', 'warranty', 'price'],
    "MPPTS": ['product_series', 'technology', 'product_type', 'voltage_min', 'panel_capacity', 'price'],
    "tubular_batteries": ['variant', 'product_type', 'Ah_rating', 'warranty', 'price', 'suitable_for'],
    "solar_batteries": ['variant', 'product_type', 'Ah_rating', 'warranty', 'price', 'suitable_for'],
    "lithium_ion_batteries": ['variant', 'product_type', 'Ah_rating', 'warranty', 'price', 'suitable_for'],
}

class FilterOptionsView(APIView):
    def get(self, request, category_slug):
        filters = SUB_CATEGORY_FILTERS.get(category_slug.lower(), [])
        return Response({'filters': filters})


class ProductsFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__category", lookup_expr="icontains")
    variant = filters.CharFilter(field_name="variant__variant_name", lookup_expr="icontains")
    price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    weight = filters.NumberFilter(field_name="weight", lookup_expr="lte")
    voltage = filters.NumberFilter(field_name="voltage", lookup_expr="lte")
    va_rating = filters.NumberFilter(field_name="va_rating", lookup_expr="gte")
    warranty = filters.CharFilter(field_name="warranty", lookup_expr="icontains")
    product_series = filters.CharFilter(field_name="product_series", lookup_expr="icontains")
    wattage = filters.CharFilter(field_name="wattage", lookup_expr="icontains")
    product_type = filters.CharFilter(field_name="type", lookup_expr="icontains")
    Ah_rating = filters.NumberFilter(field_name="Ah_rating", lookup_expr="gte")
    suitable_for = filters.CharFilter(field_name="suitable_for", lookup_expr="icontains")

    class Meta:
        model = Products
        fields = [
            'category', 'variant', 'price', 'weight', 'voltage',
            'va_rating', 'warranty', 'product_series', 'wattage', 'product_type', 'Ah_rating', 'suitable_for'
        ]


class ProductsView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter

    
    
class PreviewDetailsView(viewsets.ModelViewSet):
    queryset = PreviewDetails.objects.all()
    serializer_class = PreviewDetailsSerializer
    
    @action(detail=False, methods=['get'], url_path='category/(?P<slug>[^/.]+)')
    def by_category(self, request, slug=None):
        queryset = self.queryset.filter(category__category=slug)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class HeroCarouselView(viewsets.ModelViewSet):
    queryset = HeroCarousel.objects.all()
    serializer_class = HeroCarouselSerializer
    
    
class ContactSupportViewSet(viewsets.ModelViewSet):
    queryset = ContactSupport.objects.all()
    serializer_class = ContactSupportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Optional: send email
        support_data = serializer.validated_data
        # send_mail(
        #     subject=f"New {support_data['support_type']} Support Request",
        #     message=f"Name: {support_data['name']}\nEmail: {support_data['email']}\n\nMessage:\n{support_data['message']}",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=["support@yourcompany.com"],
        #     fail_silently=False,
        # )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(self.request.user)
        return Response({"message": "User created"}, status=201)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(self.request.user)
        return Response(serializer.validated_data)
    
    
    
def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    # Ensure the session exists (creates session_key if not)
    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key

    # Reuse the session_key to get or create a single cart
    cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart




class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        print("Session Key in Backend:", request.session.session_key)
        cart = get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        print("Session Key:", request.session.session_key)
        print("Cart items:", cart.items.all())
        return Response({'status': 'cart cleared'}, status=status.HTTP_200_OK)



class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = []  # No auth required

    def get_queryset(self):
        cart = get_or_create_cart(self.request)
        return cart.items.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart'] = get_or_create_cart(self.request)
        return context

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        cart = get_or_create_cart(request)
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # **Check cart items right after saving**
        print("Cart items AFTER adding:", cart.items.all())


        return Response(
            CartItemSerializer(cart_item, context={'cart': cart}).data,
            status=status.HTTP_201_CREATED)



    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = BuyNow.objects.all()
    serializer_class = BuyNowSerializer

    # Custom action to place an order
    @action(detail=False, methods=['post'], url_path='place-order')
    def place_order(self, request):
        """
        Place an order by creating an Order instance with the provided data.
        """
        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email')
        customer_phone = request.data.get('customer_phone')
        shipping_address = request.data.get('shipping_address')
        city = request.data.get('city')
        state = request.data.get('state')
        zip_code = request.data.get('zip_code')
        items = request.data.get('items')

        # Initialize total_amount to 0
        total_amount = Decimal(0)
        order_items = []

        # Calculate total price for the order
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            product = Products.objects.get(id=product_id)
            total_amount += product.price * quantity
            order_items.append(OrderItem(product=product, quantity=quantity))

        # Create the order
        order = BuyNow.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            city=city,
            state=state,
            zip_code=zip_code,
            total_amount=total_amount,
        )

        # Create order items
        for item in order_items:
            item.order = order
            item.save()

        # Return the created order data
        serializer = BuyNowSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)