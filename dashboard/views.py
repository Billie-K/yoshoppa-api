from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import *

# Create your views here.


#@login_required
def dashboard(request):
    """The dashboard for user admins on Gurushop"""
    return render(request, 'dashboard/index.html')

#@login_required
def profile(request):
    """A profile for the logged-in user to manage"""
    return render(request, 'dashboard/profile.html')

def products(request):
    """The products table in admin"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'dashboard/products.html', context)

def categories(request):
    """The categories table in admin"""
    categories = Categories.objects.all()
    context = {'categories': categories}
    return render(request, 'dashboard/categories.html', context)


def test(request):
    """A profile for the logged-in user to manage"""
    return render(request, 'dashboard/test.html')

def addProduct(request):
    """A profile for the logged-in user to manage"""
    return render(request, 'dashboard/add-product.html')