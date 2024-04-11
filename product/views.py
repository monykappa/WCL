
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


# Create your views here.
def products(request):
    drugs = Drug.objects.all()  # Retrieve all drugs from the database
    return render(request, 'products/products.html', {'drugs': drugs})


def product_detail(request):
    return render(request, 'products/products.html')