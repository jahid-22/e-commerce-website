from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# category Model

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug          = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse("products_by_category", args=[self.slug])
    

# Product Model
class Product(models.Model):
    name          = models.CharField(max_length=100)
    slug          = models.SlugField(max_length=100)
    selling_price = models.IntegerField()
    regular_price = models.IntegerField()
    desc          = models.TextField()
    is_availabe   = models.BooleanField(default=True)
    in_stock      = models.IntegerField()
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateField(auto_now_add=False)
    img           = models.ImageField(upload_to='projImg/')
    
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", args = [self.category.slug, self.slug, self.pk])
    
    @property
    def Prod_selling_price(self):
        return self.selling_price
    
# Cart 
class Cart(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.PROTECT)
    quantity    = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'product',)
    

# Variation Model
variation_cata_choice = (
    ('color', 'color'),
    ('size', 'size')
)
class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_catagory  = models.CharField(max_length=50, choices=variation_cata_choice)
    is_active           = models.BooleanField(default=True)
    variation_value     = models.CharField(max_length=100)
    created_date        = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    