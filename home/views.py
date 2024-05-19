from gettext import translation
from django.http import JsonResponse
from django.shortcuts import render
from news.models import *
from django.http import JsonResponse
from django.views import View
from product.models import *
from django.shortcuts import render, get_object_or_404
import random


# Create a base view class with the Category model included in the context
class BaseView(View):
    def get_context_data(self, **kwargs):
        context = {}
        # Fetch all categories and sort them alphabetically by name
        context['categories'] = Category.objects.all().order_by('name')
        context.update(kwargs)
        return context

class HomeView(BaseView):
    def get(self, request):
        news_items = New.objects.filter(is_published=True)
        all_products = list(Product.objects.all())
        random_products = random.sample(all_products, min(len(all_products), 8))  # Get up to 8 random products

        context = {
            'news_items': news_items,
            'random_products': random_products
        }
        return render(request, 'home/home.html', self.get_context_data(**context))
class AboutUsView(BaseView):
    def get(self, request):
        return render(request, 'home/about_us.html', self.get_context_data())

class ContactUsView(BaseView):
    def get(self, request):
        return render(request, 'home/contact_us.html', self.get_context_data())

class CeoMessageView(BaseView):
    def get(self, request):
        return render(request, 'home/ceo_message.html', self.get_context_data())

class TopManagementView(BaseView):
    def get(self, request):
        return render(request, 'home/top_management.html', self.get_context_data())

# Ensure the products views also inherit from BaseView and sort categories alphabetically
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