from django.db import models
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password

# Create your models here.


class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128) 
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

class MainPreview(models.Model):
    
    CATEGORY_CHOICES= [
        ("home_ups", "Home Ups"),
        ("solar_power", "Solar Power"),
        ("batteries", "Batteries"),
        ("ev_charger", "EV Charger"),
        ("water_purifier", "Water Purifier"),
        ("li_ion_battery_inverter", "Lithium Ion Battery Inverter"),
    ]
    
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.category
    
    
    
SUB_CATEGORY_CHOICES= [
    ("online_ups", "Online Ups"),
    ("offline_ups", "Offline Ups"),
    ("hkva_ups", "HKVA Ups"),
    ("solar_ups", "Solar Ups"),
    ("solar_panel", "Solar Panel"),
    ("lithium_solar_inverter", "Lithium Solar Inverter"),
    ("MPPTS", "MPPTS"),
    ("tubular_batteries", "Tubular Batteries"),
    ("solar_batteries", "Solar Batteries"),
    ("lithium_ion_batteries", "Lithium Ion Batteries"),
]
    
class PreviewDetails(models.Model):
    
    category = models.ForeignKey(MainPreview, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=100, choices=SUB_CATEGORY_CHOICES)
    variant_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True, editable=False)
    slogan = models.CharField(max_length=100, null=True, blank=True)
    feature1 = models.CharField(max_length=100)
    feature2 = models.TextField()
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.variant_name)
            slug = base_slug
            counter = 1
            while PreviewDetails.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.variant_name


class Products(models.Model):
    
    MODEL_TYPE_CHOICES = [
        ("WR", "WR"),
        ("NG", "NG"),
    ]
    
    category = models.ForeignKey(MainPreview, on_delete=models.CASCADE )
    subcategory = models.CharField(max_length=100, choices=SUB_CATEGORY_CHOICES )
    variant=models.ForeignKey(PreviewDetails, on_delete=models.CASCADE,related_name='products_by_variant' )
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/')
    image2=models.ImageField(upload_to='images/', default=0 ,null=True, blank=True)
    image3=models.ImageField(upload_to='images/', default=0 ,null=True , blank=True)
    model_type = models.CharField(max_length=10, choices=MODEL_TYPE_CHOICES , null=True, blank=True)
    model_number = models.CharField(max_length=100 , null=True, blank=True)
    price=models.IntegerField()
    old_price=models.IntegerField()
    weight=models.FloatField(default=0)
    voltage=models.FloatField(default=0)
    dimensions=models.CharField(max_length=100,default=0)
    features=models.TextField(default=0)
    description=models.TextField(default=0)
    additional_info=models.TextField(default=0)
    technical_spec=models.TextField(default=0)
    new_arrival=models.BooleanField(default=False)
    # newly added for filter
    va_rating =models.FloatField(default=0, null=True, blank=True)
    warranty = models.CharField(max_length=100, default=0, null=True, blank=True)
    product_series = models.CharField(max_length=100, default=0, null=True, blank=True)
    wattage = models.CharField(max_length=100, default=0, null=True, blank=True)
    product_type = models.CharField(max_length=100, default=0, null=True, blank=True)
    suitable_for = models.CharField(max_length=100, default=0, null=True, blank=True)
    technology = models.CharField(max_length=100, default=0, null=True, blank=True)
    panel_capacity = models.CharField(max_length=100, default=0, null=True, blank=True)
    Ah_rating = models.CharField(max_length=100, default=0, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class HeroCarousel(models.Model):
    image=models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.image.name if self.image else "No Image"
    
    

class ContactSupport(models.Model):
    SUPPORT_CHOICES = [
        ('installation', 'Product Installation'),
        ('complaint', 'Complaint Registration'),
        ('service', 'General Service Request'),
        ('amc', 'AMC Request'),
        ('business', 'Business Enquiry'),
    ]

    support_type = models.CharField(max_length=20, choices=SUPPORT_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.support_type}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('Products', through='CartItem')

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"{self.user.username}'s Cart" if self.user else f"Session Cart ({self.session_key})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product')

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    
class BuyNow(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(BuyNow, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item {self.product.title} in Order {self.order.id}"
    
