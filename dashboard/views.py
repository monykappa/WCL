from multiprocessing import AuthenticationError
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import *
from product.models import *
from news.models import *
from .models import *
from django.views.decorators.http import require_POST
from django.views import View
from django.utils.decorators import method_decorator
import pycountry
from django.conf import settings
import csv
import openpyxl
import requests
from openpyxl.drawing.image import Image
from io import BytesIO
import os
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, 'dashboard/error_pages/403.html', status=403)

class EditUserView(SuperuserRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'dashboard/edit_page/edit_user.html', {'user': user})
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        # Handle form submission and save changes
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.save()
        return redirect('dashboard:user')  # Redirect to the user list page after saving changes
    
class UserView(View):
    template_name = 'dashboard/user.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {'users': users})

    def post(self, request):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_superuser = request.POST.get('superuser') == 'true'  # Convert 'true' string to boolean
        is_active = request.POST.get('active') == 'true'
        is_staff = request.POST.get('staff') == 'true'

        if not all([username, first_name, last_name, email, password, confirm_password]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
        
        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        # Create a new user instance
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.is_staff = is_staff
        user.save()
        return JsonResponse({'status': 'success', 'user_id': user.id})
    
    
class DeleteUserView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('dashboard:user') 


def export_to_excel(request):
    # Create a new Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active

    # Add headers
    ws.append(['Name', 'Description', 'Manufacturer', 'Price', 'Quantity Available', 'Expiry Date', 'Category', 'Drug Type'])

    # Add data rows
    products = Drug.objects.all()
    for product in products:
        ws.append([product.name, product.description, product.manufacturer.name, product.price, product.quantity_available, product.expiry_date, product.category.name, product.drug_type.name])

    # Define the directory to save the Excel file
    exports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'exports')
    os.makedirs(exports_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Save the workbook to a file
    excel_file_path = os.path.join(exports_dir, 'products.xlsx')
    wb.save(excel_file_path)

    # Open the file and serve it as an HttpResponse
    with open(excel_file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    return response

# Sign in
class SignInView(View):
    def get(self, request):
        return render(request, "dashboard/sign_in.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password'})
# Log out
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('dashboard:sign_in')


# def dashboard_base(request):
#     return render(request, 'dashboard/dashboard_base.html')

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        latest_products = Drug.objects.order_by('-created_at')[:5]
        latest_categories = Category.objects.order_by('-created_at')[:5]
        latest_manufacturers = Manufacturer.objects.order_by('-created_at')[:5]
        latest_product_types = DrugType.objects.order_by('-created_at')[:5]

        context = {
            'latest_products': latest_products,
            'latest_categories': latest_categories,
            'latest_manufacturers': latest_manufacturers,
            'latest_product_types': latest_product_types,
        }

        return render(request, 'dashboard/overview.html', context)

# Products
@method_decorator(login_required, name='dispatch')
class ProductsView(View):
    def get(self, request):
        # Fetch all products from the database
        products = Drug.objects.all()
        manufacturers = Manufacturer.objects.all()  # Retrieve all manufacturers
        categories = Category.objects.all()  # Retrieve all categories
        drug_types = DrugType.objects.all()  # Retrieve all drug types
        
        category_filter = request.GET.get('category')
        if category_filter:
            # Filter products by the selected category
            products = products.filter(category__name=category_filter)
            
        return render(request, 'dashboard/products.html', {'products': products, 'manufacturers': manufacturers, 'categories': categories, 'drug_types': drug_types})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:products')
        return render(request, 'dashboard/add_page/add_product.html', {'form': form})
    


class ProductDetailsView(View):
    def get(self, request, product_id):
        try:
            product = Drug.objects.get(pk=product_id)
            # Generate image URL
            if product.image:
                image_url = settings.MEDIA_URL + str(product.image)
            else:
                image_url = None
            # Prepare product data
            product_data = {
                'name': product.name,
                'slug': product.slug,  # Include the slug attribute
                'image': image_url,
                'description': product.description,
                'manufacturer': product.manufacturer.name,
                'price': product.price,
                'quantity_available': product.quantity_available,
                'expiry_date': product.expiry_date,
                'category': product.category.name,
                'drug_type': product.drug_type.name,
            }
            # Return JSON response with product data
            return JsonResponse(product_data)
        except Drug.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)




class EditProductView(SuperuserRequiredMixin, View):
    def get(self, request, slug):
        product = get_object_or_404(Drug, slug=slug)
        form = ProductForm(instance=product)
        return render(request, 'dashboard/edit_page/edit_product.html', {'form': form})

    def post(self, request, slug):
        product = get_object_or_404(Drug, slug=slug)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_instance = form.save(commit=False)

            # Check if a new image is uploaded
            new_image = form.cleaned_data.get('image')
            if new_image:
                # Update the existing image field with the new image
                product_instance.image = new_image

            # Save the form instance to the database
            try:
                product_instance.save()
            except ValidationError as e:
                # If there's a validation error, render the form with the error message
                form.add_error(None, e)

            return redirect('dashboard:products')
        return render(request, 'dashboard/edit_page/edit_product.html', {'form': form})
    
    
class DeleteProductView(SuperuserRequiredMixin, View):
    def post(self, request, slug):
        # Retrieve the product
        product = get_object_or_404(Drug, slug=slug)
        
        # Delete the product
        product.delete()
        
        # Return a success message
        return redirect('dashboard:products')




# category
@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'dashboard/category.html', {'categories': categories})


    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category')
        return render(request, 'dashboard/add_page/add_category.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class EditCategoryView(SuperuserRequiredMixin, View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        form = CategoryForm(instance=category)
        return render(request, 'dashboard/edit_page/edit_category.html', {'form': form})

    def post(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category')
        return render(request, 'dashboard/edit_page/edit_category.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DeleteCategoryView(SuperuserRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect('dashboard:category')

# @method_decorator(login_required, name='dispatch')
# class AddCategoryView(View):
#     def get(self, request):
#         form = CategoryForm()
#         return render(request, 'dashboard/add_page/add_category.html', {'form': form})

#     def post(self, request):
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard:category')
#         return render(request, 'dashboard/add_page/add_category.html', {'form': form})



# Manufacturer
@method_decorator(login_required, name='dispatch')
class ManufacturerView(View):
    def get(self, request):
        form = ManufacturerForm()
        country_choices = [(country.alpha_2, country.name) for country in pycountry.countries]
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            manufacturer_id = request.GET.get('manufacturer_id')
            try:
                manufacturer = Manufacturer.objects.get(id=manufacturer_id)
                data = {
                    'name': manufacturer.name,
                    'country': manufacturer.get_country_display(),
                    'description': manufacturer.description,
                }
                return JsonResponse(data)
            except Manufacturer.DoesNotExist:
                return JsonResponse({'error': 'Manufacturer not found'}, status=404)
        else:
            manufacturers = Manufacturer.objects.all()
            return render(request, 'dashboard/manufacturer.html', {'manufacturers': manufacturers, 'form': form, 'country_choices': country_choices})

    def post(self, request):
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'success': 'Manufacturer added successfully'})
            else:
                return redirect('dashboard:manufacturer')
        else:
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                errors = form.errors.as_json()
                return JsonResponse({'errors': errors}, status=400)
            else:
                return render(request, 'dashboard/manufacturer.html', {'form': form})



@method_decorator(login_required, name='dispatch')
class EditManufacturerView(SuperuserRequiredMixin, View):
    def get(self, request, manufacturer_slug):
        manufacturer = get_object_or_404(Manufacturer, slug=manufacturer_slug)
        form = ManufacturerForm(instance=manufacturer)
        return render(request, 'dashboard/edit_page/edit_manufacturer.html', {'form': form})

    def post(self, request, manufacturer_slug):
        manufacturer = get_object_or_404(Manufacturer, slug=manufacturer_slug)
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manufacturer')  # Assuming this redirects to the manufacturer list page
        return render(request, 'dashboard/edit_page/edit_manufacturer.html', {'form': form})



@method_decorator(login_required, name='dispatch')
class DeleteManufacturerView(SuperuserRequiredMixin, View):
    def post(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
        manufacturer.delete()
        return redirect('dashboard:manufacturer')

# Product type
class ProductTypeView(View):
    def get(self, request):
        form = DrugTypeForm()
        drug_types = DrugType.objects.all()
        return render(request, 'dashboard/product_type.html', {'form': form, 'drug_types': drug_types})

    def post(self, request):
        form = DrugTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # Return JSON response for success
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})  # Return JSON response for errors



@method_decorator(login_required, name='dispatch')
class EditProductTypeView(SuperuserRequiredMixin, View):
    def get(self, request, slug):
        drug_type = get_object_or_404(DrugType, slug=slug)
        form = DrugTypeForm(instance=drug_type)
        return render(request, 'dashboard/edit_page/edit_product_type.html', {'form': form})

    def post(self, request, slug):
        drug_type = get_object_or_404(DrugType, slug=slug)
        form = DrugTypeForm(request.POST, instance=drug_type)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product_type')
        return render(request, 'dashboard/edit_page/edit_product_type.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DeleteProductTypeView(View):
    def post(self, request, drug_type_id):
        drug_type = get_object_or_404(DrugType, id=drug_type_id)
        drug_type.delete()
        return redirect('dashboard:product_type')

# News
@method_decorator(login_required, name='dispatch')
class NewsView(View):
    def get(self, request):
        # Handle GET request to display news list and add news form
        news_items = New.objects.all().order_by('-updated_at')
        form = NewsForm()
        return render(request, 'dashboard/news.html', {'news_items': news_items, 'form': form})

    def post(self, request):
        # Handle POST request to add new news
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_instance = form.save(commit=False)
            if 'publishCheckbox' in request.POST:
                news_instance.is_published = True
            news_instance.save()
            return redirect('dashboard:news')  # Redirect to news list after adding news
        # If form is invalid, render the news list with the form again
        news_items = New.objects.all().order_by('-updated_at')
        return render(request, 'dashboard/news.html', {'news_items': news_items, 'form': form})

@method_decorator(login_required, name='dispatch')
class AddNewsView(SuperuserRequiredMixin, View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'dashboard/add_page/add_news.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_instance = form.save(commit=False)
            if 'publishCheckbox' in request.POST:
                news_instance.is_published = True
            news_instance.save()
            return redirect('dashboard:news')
        return render(request, 'dashboard/add_page/add_news.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class EditNewsView(SuperuserRequiredMixin, View):
    def post(self, request, new_slug):
        new = get_object_or_404(New, slug=new_slug)
        form = NewsForm(request.POST, request.FILES, instance=new)
        # Capture previous values before saving the form
        previous_title = new.title
        previous_image = new.image
        previous_description = new.description
        if form.is_valid():
            news_instance = form.save(commit=False)
            if 'publishCheckbox' in request.POST:
                news_instance.is_published = True
            else:
                news_instance.is_published = False  # Update is_published field if checkbox is unchecked
            form.save()

            # Create UpdateHistory object with previous and new values
            UpdateHistory.objects.create(
                news=new,
                user=request.user,
                title_before=previous_title,
                image_before=previous_image,
                description_before=previous_description,
                title_after=new.title,
                image_after=new.image,
                description_after=new.description
            )

            return redirect('dashboard:news')
        return render(request, 'dashboard/edit_page/edit_news.html', {'form': form, 'new': new})

    def get(self, request, new_slug):
        new = get_object_or_404(New, slug=new_slug)
        form = NewsForm(instance=new)
        return render(request, 'dashboard/edit_page/edit_news.html', {'form': form, 'new': new})

@method_decorator(login_required, name='dispatch')
class UpdateHistoryView(View):
    def get(self, request, new_slug):
        new_instance = get_object_or_404(New, slug=new_slug)
        update_history_entries = new_instance.updatehistory_set.all().order_by('-update_time')
        return render(request, 'dashboard/history/update_new_history.html', {'new': new_instance, 'update_history_entries': update_history_entries})

@method_decorator(login_required, name='dispatch')
class DeleteNewsView(SuperuserRequiredMixin, View):
    def post(self, request, new_id):
        new = get_object_or_404(New, id=new_id)
        new.delete()
        return redirect('dashboard:news')