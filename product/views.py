
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


# Create your views here.
def products(request):
    products = Product.objects.all()  # Retrieve all drugs from the database
    return render(request, 'products/products.html', {'products': products})


def product_detail(request):
    return render(request, 'products/products.html')