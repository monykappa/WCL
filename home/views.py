from gettext import translation
from django.http import JsonResponse
from django.shortcuts import render
from news.models import *
from django.http import JsonResponse
from django.views import View



# class BaseView(View):
#     def get(self, request):
#         return render(request, 'base.html')

class HomeView(View):
    def get(self, request):
        news_items = New.objects.filter(is_published=True)
        return render(request, 'home/home.html', {'news_items': news_items})

class AboutUsView(View):
    def get(self, request):
        return render(request, 'home/about_us.html')

class ContactUsView(View):
    def get(self, request):
        return render(request, 'home/contact_us.html')

class CeoMessageView(View):
    def get(self, request):
        return render(request, 'home/ceo_message.html')


class TopManagementView(View):
    def get(self, request):
        return render(request, 'home/top_management.html')