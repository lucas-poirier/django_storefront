from django.urls import path
from .views import product_list
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('', product_list, name='product_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]