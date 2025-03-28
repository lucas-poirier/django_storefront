from .models import Product, Cart, CartItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegisterForm

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    else:
        cart_items = []
    return render(request, 'shop/product_list.html', {'products': products, 'cart_items': cart_items})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)  # Automatically log in the new user
            return redirect("product_list")  # Redirect to product list or another page
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def custom_login(request):
    if request.method == "POST":
        user = login(request)
        Cart.objects.get_or_create(user=user)
        return redirect("product_list")
    
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created and cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("product_list")

@login_required
def remove_one_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

    return redirect("product_list")

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        cart_item.delete()

    return redirect("cart_detail")

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})

def buy(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    missing_items = []
    for cart_item in cart_items:
        product = cart_item.product
        if product.stock < cart_item.quantity:
            missing_items.append(product)
            cart_item.delete()
            
        else:
            product.stock -= cart_item.quantity
            product.save()


    if missing_items:
        return render(request, "cart/buy.html", {"missing_items": missing_items})
    else:
        cart.delete()
        return render(request, "cart/buy.html")