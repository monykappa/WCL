from django import forms
from product.models import *
from news.models import *

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'country', 'description']
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        

class DrugTypeForm(forms.ModelForm):
    class Meta:
        model = DrugType
        fields = ['name', 'description']


class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'image', 'description']  # Specify the fields you want in the form
