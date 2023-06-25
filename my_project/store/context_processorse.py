from . models import Category, Cart

def menu_links(request):
    link =Category.objects.all()
    return {'links': link}

def cart_count(request):
    cart_counter = 0
    cart_counteing = Cart.objects.filter(user=request.user)
    for cart in cart_counteing:
        temp_count = cart.quantity
        cart_counter += temp_count
    return {'cart_counter' : cart_counter}
    

