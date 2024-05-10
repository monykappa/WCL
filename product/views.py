
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


# Create your views here.
def products(request):
    products = Product.objects.all().prefetch_related('compositions', 'pack_sizes')  # Prefetch related data to optimize database queries
    context = {'products': products}
    return render(request, 'products/products.html', context)


def product_detail(request):
    return render(request, 'products/products.html')