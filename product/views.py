
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import *


class BaseView(View):
    def get_context_data(self, **kwargs):
        # Fetch all categories and sort them alphabetically by name
        categories = Category.objects.all().order_by('name')
        context = {'categories': categories}
        context.update(kwargs)
        return context

class ProductsView(BaseView):
    def get(self, request):
        context = self.get_context_data()
        return render(request, 'products/products.html', context)

class CategoryPageView(BaseView):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        products = category.product_set.all()
        context = self.get_context_data(category=category, products=products)
        return render(request, 'products/category/category_page.html', context)



# def product_detail(request):
#     return render(request, 'products/products.html')
