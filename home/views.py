from gettext import translation
from django.http import JsonResponse
from django.shortcuts import render
from news.models import *
from django.http import JsonResponse
from django.views import View
from product.models import *



# Create a base view class with the Category model included in the context
class BaseView(View):
    def get_context_data(self, **kwargs):
        context = {}
        context['categories'] = Category.objects.all()
        context.update(kwargs)
        return context

# Modify each view to inherit from the BaseView class
class HomeView(BaseView):
    def get(self, request):
        news_items = New.objects.filter(is_published=True)
        context = {'news_items': news_items}
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

