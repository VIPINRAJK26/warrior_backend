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
import razorpay
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
import pkg_resources
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.decorators.csrf import csrf_exempt

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
    "online_ups": ['variant', 'va_rating', 'voltage', 'warranty', 'price'],
    "offline_ups": ['variant', 'va_rating', 'voltage', 'warranty', 'price'],
    "hkva_ups": ['variant', 'va_rating', 'voltage', 'warranty', 'price'],
    "solar_ups": ['variant', 'va_rating', 'voltage', 'warranty', 'price'],
    "solar_panel": ['product_series', 'voltage', 'wattage', 'price'],
    "lithium_solar_inverter": ['variant', 'va_rating', 'voltage', 'warranty', 'price'],
    "MPPTS": ['product_series', 'technology', 'product_type', 'voltage', 'panel_capacity', 'price'],
    "tubular_batteries": ['variant', 'product_type', 'Ah_rating', 'warranty', 'price', 'suitable_for'],
    "solar_batteries": ['variant', 'product_type', 'Ah_rating', 'warranty', 'price', 'suitable_for'],
    "lithium_ion_batteries": ['variant', 'product_type', 'Ah_rating', 'warranty', 'price', 'suitable_for'],
}


class FilterOptionsView(APIView):
    def get(self, request, subcategory_slug):
        filters = SUB_CATEGORY_FILTERS.get(subcategory_slug.lower(), [])
        return Response({'filters': filters})


class ProductsFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__category", lookup_expr="icontains")
    variant = filters.CharFilter(field_name="variant__variant_name", lookup_expr="icontains")
    price = filters.NumberFilter(field_name="price", lookup_expr="gte")
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
            'category', 'variant', 'price', 'voltage',
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
    print("get_or_create_cart called")
    if request.user.is_authenticated:
        print("Authenticated user:", request.user)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    session_key = request.data.get('session_key') or request.query_params.get('session_key')
    print("Session key:", session_key)
    if not session_key:
        print("No session key found for anonymous user")
        return None
    cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart








class CartView(APIView):
    def get(self, request):
        cart = get_or_create_cart(request)
        if not cart:
            return Response({'error': 'Missing session_key'}, status=400)

        serializer = CartSerializer(cart)
        return Response(serializer.data)



class CartItemView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        print("CartItemView POST called")
        cart = get_or_create_cart(request)
        if not cart:
            print("Missing session_key or user not authenticated")
            return Response({'error': 'Missing session_key'}, status=400)

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        print(f"product_id: {product_id}, quantity: {quantity}")

        if not product_id:
            print("No product_id provided")
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            print("Product not found")
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def patch(self, request, pk=None):
        cart = get_or_create_cart(request)
        if not cart:
            return Response({'error': 'Missing session_key'}, status=400)

        try:
            cart_item = CartItem.objects.get(id=pk, cart=cart)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=404)

        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_item.quantity = quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        cart = get_or_create_cart(request)
        if not cart:
            return Response({'error': 'Missing session_key'}, status=400)

        try:
            cart_item = CartItem.objects.get(id=pk, cart=cart)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=404)

        cart_item.delete()
        return Response({'success': 'Item removed'})

class ClearCartView(APIView):
    def post(self, request):
        cart = get_or_create_cart(request)
        if not cart:
            return Response({'error': 'Missing session_key'}, status=400)

        cart.cart_items.all().delete()
        return Response({'message': 'Cart cleared successfully'}, status=200)





    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = BuyNow.objects.all()
    serializer_class = BuyNowSerializer

    # Custom action to place an order
    @action(detail=False, methods=['post'], url_path='place-order')
    def place_order(self, request):
        items = request.data.get('items')
        if not items:
            return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        required_fields = ['customer_name', 'customer_email', 'customer_phone', 'shipping_address', 'city', 'state', 'zip_code']
        for field in required_fields:
            if not request.data.get(field):
                return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email')
        customer_phone = request.data.get('customer_phone')
        shipping_address = request.data.get('shipping_address')
        city = request.data.get('city')
        state = request.data.get('state')
        zip_code = request.data.get('zip_code')

        total_amount = Decimal(0)
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                return Response({"error": f"Product with id {product_id} not found."}, status=status.HTTP_400_BAD_REQUEST)

            total_amount += product.price * quantity

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

        for item in items:
            product = Products.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )

        serializer = BuyNowSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    

@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_razorpay_order(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount = Decimal(request.data.get("amount", 0))
    if amount <= 0:
        return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
    currency = "INR"

    razorpay_order = client.order.create({
        "amount": int(amount * 100),  
        "currency": currency,
        "payment_capture": 1
    })

    return Response({
        "id": razorpay_order["id"],
        "amount": razorpay_order["amount"],
        "currency": razorpay_order["currency"]
    }, status=status.HTTP_200_OK)
