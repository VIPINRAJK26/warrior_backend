from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email


class MainPreview(models.Model):
    
    CATEGORY_CHOICES= [
        ("home_inverter_and_ups", "Home Inverter/Ups"),
        ("lithium_inverter_and_ups", "Lithium Inverter/Ups"),
        ("solar_power", "Solar Power"),
        ("batteries", "Batteries"),
        ("li_ion_batteries", "Lithium Ion Batteries"),
        ("ev_charger", "EV Charger"),
        ("water_purifier", "Water Purifier"),
    ]
    
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.category
    
    
SUB_CATEGORY_CHOICES= [
    ("online_inverter_and_ups", "Online Inverter/Ups"),
    ("offline_inverter_and_ups", "Offline Inverter/Ups"),
    ("hkva_ups", "HKVA Ups"),
    ("avr_ups", "AVR Ups"),
    ("solar_ups", "Solar Ups"),
    ("solar_panel", "Solar Panel"),
    ("lithium_solar_inverter", "Lithium Solar Inverter"),
    ("MPPTS", "MPPTS"),
    ("tubular_batteries", "Tubular Batteries"),
    ("solar_batteries", "Solar Batteries"),
    ("lithium_ion_batteries", "Lithium Ion Batteries"),
    ("lithium_batteries", "Lithium Batteries"),
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
    brochure = models.FileField(upload_to='brochures/', null=True, blank=True)
  
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
    features=models.TextField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    additional_info=models.TextField(null=True,blank=True)
    technical_spec=models.TextField(null=True,blank=True)
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

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    support_type = models.CharField(max_length=20, choices=SUPPORT_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.name} - {self.support_type} - {self.status}"


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
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
    
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    est_delivery = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.customer_name} - {self.status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(BuyNow, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item {self.product.title} in Order {self.order.id}"
    
    
class Invoice(models.Model):
    order = models.OneToOneField('BuyNow', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice {self.invoice_number} for Order {self.order.id}"
    
    def get_url(self):
        if self.invoice_file:
            return self.invoice_file.url
        return None
    
    

class ModelNumberAndWarrenty(models.Model):
    model_number = models.CharField(max_length=100)
    warrenty = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.model_number


class StateSelection(models.Model):
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.state


class DistrictSelection(models.Model):
    state = models.ForeignKey(StateSelection, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.district


class Dealer(models.Model):
    district = models.ForeignKey(DistrictSelection, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ProductType(models.Model):
    product_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_type



class WarrentyRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)

    address = models.TextField()
    state = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    pin_code = models.CharField(max_length=10,null=True,blank=True)

    product_type = models.CharField(max_length=100,null=True,blank=True)

    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)

    purchase_date = models.DateField()

    warranty_period_months = models.PositiveIntegerField(null=True,blank=True)
    warranty_end_date = models.DateField(null=True,blank=True)

    dealer = models.CharField(max_length=100,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
