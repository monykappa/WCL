from gettext import translation
from django.http import JsonResponse
from django.shortcuts import render
from news.models import *
from django.http import JsonResponse



def base(request):
    return render(request, 'base.html')


def home(request):
    news_items = News.objects.all()
    return render(request, 'home/home.html', {'news_items': news_items})
