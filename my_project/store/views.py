from django.shortcuts import render, redirect
from . models import Category, Product, Cart
from django.db.models import Q
from django.http import JsonResponse, Http404 , HttpResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

# Home

def home(request):
    all_prod = Product.objects.all().filter(is_availabe=True)
    for prod in all_prod:
        m = prod 
        print(m.selling_price)
    return render(request, 'index.html', {'all_prod': all_prod})

# product detail


def products_detail(request, category, product, id):

    try:
        # bring product form Product Model...
        get_prod = Product.objects.get(
            category__slug=category, slug=product, pk=id)
    except Exception as e:
        raise e

    return render(request, 'product-detail.html', {'get_prod': get_prod})

# store


def store(request, category_name=None):
    prod_count = None  # Initializeing prod_count
    categoreis = None
    if category_name == None:
        products = Product.objects.all().filter(is_availabe=True)
        prod_count = products.count()
        
        # paginator
        paginator = Paginator(products, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
    else:
        try:
            # categoreis = get_object_or_404(Category, slug=category_name)
            products = Product.objects.filter(category__slug=category_name).order_by('-created_at')
            paginator = Paginator(products, 6)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            prod_count = products.count()
            print(page_obj.previous_page_number)
        except Exception as e:
            raise e

    context = {
        'get_prod': page_obj,
        'prod_count': prod_count,
    }
    return render(request, 'store.html', context)

# get product session key


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# add to cart


def add_to_cart(request, product_id=None):
    
    # selected colors & size
    color = request.GET.get('color')
    size = request.GET.get('size')
    return HttpResponse(color + ' ' + size)
    exit()
    
    user=request.user
    if product_id != None:
        product = Product.objects.get(id=product_id)
        user=request.user

        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(Q(product=product) & Q(user=user))
                if cart:
                    cart.quantity += 1
                    cart.save()
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    user=user, product=product
                )
            cart.save()

    get_single_product = Cart.objects.filter(user=user)

    total_amount = 0.0
    amount = 0.0
    shiping_fee = 100
    # exiting_quantity = [p for p in Cart.objects.all() if p.user == request.user]
    exiting_quantity = Cart.objects.filter(user=user)
    for p in exiting_quantity:
        temp_amount = (p.quantity * p.product.selling_price)
        amount += temp_amount

    context = {
        'get_single_product': get_single_product,
        'amount': amount,
        'total_amount': amount + shiping_fee
    }

    return render(request, 'cart.html', context)

# plus cart


def plus_cart(request):
    prod_id = request.GET['prod_id']
    user=request.user

    try:
        cart = Cart.objects.get(Q(id=prod_id) & Q(user=user))
        cart.quantity += 1
        cart.save()
    except Cart.DoesNotExist:
        raise Http404

    total_amount = 0.0
    amount = 0.0
    shiping_fee = 100
    # exiting_quantity = [p for p in Cart.objects.all() if p.user == request.user]
    exiting_quantity = Cart.objects.filter(user=user)
    for p in exiting_quantity:
        temp_amount = (p.quantity * p.product.selling_price)
        amount += temp_amount
    
    data = {
        'quantity': cart.quantity,
        'amount': amount,
        'total_amount': amount + shiping_fee
    }

    return JsonResponse(data)

# minus cart


def minus_cart(request):
    prod_id = request.GET['prod_id']
    user=request.user

    try:
        cart = Cart.objects.get(Q(id=prod_id) & Q(user=user))
        cart.quantity -= 1
        cart.save()
    except Cart.DoesNotExist:
        raise Http404

    total_amount = 0.0
    amount = 0.0
    shiping_fee = 100
    # exiting_quantity = [p for p in Cart.objects.all() if p.user == request.user]
    exiting_quantity = Cart.objects.filter(user=user)
    for p in exiting_quantity:
        temp_amount = (p.quantity * p.product.selling_price)
        amount -= temp_amount
    
    data = {
        'quantity': cart.quantity,
        'amount': amount,
        'total_amount': amount + shiping_fee
    }

    return JsonResponse(data)


# minus cart


def remove_cart(request):
    prod_id = request.GET['prod_id']
    user=request.user

    try:
        cart = Cart.objects.get(Q(id=prod_id) & Q(user=user))
        cart.delete()
    except Cart.DoesNotExist:
        raise Http404

    total_amount = 0.0
    amount = 0.0
    shiping_fee = 100
    # exiting_quantity = [p for p in Cart.objects.all() if p.user == request.user]
    exiting_quantity = Cart.objects.filter(user=user)
    for p in exiting_quantity:
        temp_amount = (p.quantity * p.product.selling_price)
        amount -= temp_amount
    
    data = {
        'quantity': cart.quantity,
        'amount': amount,
        'total_amount': amount + shiping_fee
    }

    return JsonResponse(data)
