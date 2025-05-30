from rest_framework import serializers
from warrior_app.models import MainPreview, Products, PreviewDetails, HeroCarousel,ContactSupport,User,Cart,CartItem,BuyNow,OrderItem,SUB_CATEGORY_CHOICES
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class MainPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPreview
        fields = "__all__" 
        
class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=MainPreview.objects.all(), slug_field='category'
    )
    variant = serializers.SlugRelatedField(
        queryset=PreviewDetails.objects.all(), slug_field='slug'
    )
    subcategory = serializers.SerializerMethodField()
    variant_slug = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = "__all__"

    def get_variant_slug(self, obj):
        return obj.variant.slug if obj.variant else None

    def get_subcategory(self, obj):
        return obj.subcategory



        
class PreviewDetailsSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MainPreview.objects.all(), source='category', write_only=True
    )
    category = serializers.SlugRelatedField(
        slug_field='category', read_only=True
    )
    subcategory = serializers.ChoiceField(
        choices=SUB_CATEGORY_CHOICES, read_only=True
    )

    class Meta:
        model = PreviewDetails
        fields = "__all__"



class HeroCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroCarousel
        fields = "__all__"
        
        
class ContactSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSupport
        fields = "__all__"
        
        
        
# accounts/serializers.py


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}  # Hides password in browsable API
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate(self, data):
        # Password confirmation check
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        
        # Email uniqueness check
        if User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError("Email already in use")
        
        # Username uniqueness check
        if User.objects.filter(username__iexact=data['username']).exists():
            raise serializers.ValidationError("Username already taken")
            
        return data

    def create(self, validated_data):
        # Remove password2 (only used for validation)
        validated_data.pop('password2')
        
        # Create user instance
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        
        # Hash password using your model's set_password()
        user.set_password(validated_data['password'])
        
        user.save()
        return user


# serializers.py

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username_or_email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        self.user = user 

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email
            }
        }



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'cart']



class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    # Automatically assign the current user if authenticated
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Make session_key optional
    session_key = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total_price', 'user', 'session_key']

    def get_total_price(self, obj):
        return obj.total_price()




    
    
class BuyNowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyNow
        fields = "__all__"
        

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"