from .models import Product
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

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
