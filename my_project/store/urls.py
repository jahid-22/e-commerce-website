from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('product-detail/<slug:category>/<slug:product>/<int:id>/', views.products_detail, name="product_detail"),
    path('store/', views.store, name="store"),
    path('store/<slug:category_name>/', views.store, name="products_by_category"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.add_to_cart, name="cart"),
    path('pluscart/', views.plus_cart, name="pluscart"),
    path('minuscart/', views.minus_cart, name="minuscart"),
    path('removecart/', views.remove_cart, name="removecart"),
    
] 


