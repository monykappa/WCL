from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

# Create your views here.
class GalleryView(TemplateView):
    template_name = 'home/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['galleries'] = Gallery.objects.all()
        return context
