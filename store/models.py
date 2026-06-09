from django.db import models
from django.urls import reverse
from jupyterlab_server import slugify

class Category(models.Model):
    name=models.CharField(max_length=120)
    slug=models.SlugField(unique=True)
    image_label=models.CharField(max_length=40, blank=True, help_text='Text shown on demo category image')
    class Meta: verbose_name_plural='Categories'
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('store:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category=models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name=models.CharField(max_length=220)
    slug=models.SlugField(unique=True)
    brand=models.CharField(max_length=120, blank=True)
    description=models.TextField(blank=True)
    base_price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='products/', blank=True, null=True)
    colour=models.CharField(max_length=80, blank=True)
    is_featured=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta: ordering=['-created_at']
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('store:product_detail', args=[self.slug])
    @property
    def total_stock(self): return sum(v.stock for v in self.variants.all())
    

class ProductVariant(models.Model):
    product=models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size=models.CharField(max_length=50, default='One Size')
    price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock=models.PositiveIntegerField(default=0)
    sku=models.CharField(max_length=80, blank=True)
    class Meta: unique_together=('product','size')
    def __str__(self): return f'{self.product.name} - {self.size}'
    @property
    def final_price(self): return self.price if self.price is not None else self.product.base_price

class Order(models.Model):
    STATUS_CHOICES=[('new','New'),('paid','Paid'),('shipped','Shipped'),('cancelled','Cancelled')]
    full_name=models.CharField(max_length=160)
    email=models.EmailField()
    phone=models.CharField(max_length=40, blank=True)
    address=models.TextField()
    city=models.CharField(max_length=100)
    postcode=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self): return f'Order #{self.id} - {self.full_name}'

class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant=models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    def line_total(self): return self.price * self.quantity
