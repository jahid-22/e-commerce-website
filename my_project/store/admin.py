from django.contrib import admin
from .models import Category, Product , Cart, Variation
# Register your models here.


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['id', 'category_name','slug']
    prepopulated_fields  = {'slug':['category_name']}
    search_fields = ['category_name']
    list_filter = ['category_name']
    

@admin.register(Product)
class AdminProdct(admin.ModelAdmin):
    list_display = ['id','name','category','slug','is_availabe','selling_price','created_date']
    search_fields = ['category','created_date']
    prepopulated_fields = {'slug':['name']}
    list_filter = ['created_date','category']

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'user']


@admin.register(Variation)
class AdminVariation(admin.ModelAdmin):
    list_display  = ['id', 'product','variation_catagory','is_active', 'created_date','variation_value']
    list_editable = ('is_active',)
    list_filter   = ('id', 'product','variation_catagory','created_date')