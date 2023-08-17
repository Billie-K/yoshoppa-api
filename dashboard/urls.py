"""Defines URL patterns for the GuruShop dashboard"""

from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    #Dashboard Home
    path('', views.dashboard, name='dash_index'),

    #Users Profile
    path('profile/', views.profile, name='profile'),

    #Products Page
    path('products/', views.products, name='products'),

    #Categories Page
    path('categories/', views.categories, name='categories'),

    #Test Page
    path('test/', views.test, name='test'),

    #Add Product Page
    path('add-product/', views.addProduct, name='add-product'),

]