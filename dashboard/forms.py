from django import forms
from product.models import *
from news.models import *

class ManufacturerForm(forms.ModelForm):
    country = CountryField().formfield()  # This will generate the appropriate form field for the CountryField

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
        fields = ['title', 'image', 'description'] 
        
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'image', 'description', 'manufacturer', 'price', 'quantity_available', 'expiry_date', 'category', 'drug_type']



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
