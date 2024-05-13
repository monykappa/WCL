from multiprocessing import AuthenticationError
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import *
from product.models import *
from gallery.models import Gallery, Image as GalleryImage

from .forms import GalleryForm, Image

from django.core.exceptions import ObjectDoesNotExist
from news.models import *
from .models import *
from django.views.decorators.http import require_POST
from django.views import View
from django.utils.decorators import method_decorator
import pycountry  # type: ignore
from django.conf import settings
import csv
import openpyxl  # type: ignore
import requests
from openpyxl.drawing.image import Image # type: ignore
from io import BytesIO
import os
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden


# Denied access if user is not a superuser
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return render(self.request, 'dashboard/error_pages/403.html', status=403)

# User
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
    
class DeleteUserView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('dashboard:user') 


# Export products to excel
class ExportToExcelView(TemplateView):
    template_name = "export_to_excel.html"

    def get(self, request, *args, **kwargs):
        # Create a new Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active

        # Add headers
        ws.append(['Name', 'Description', 'Manufacturer', 'Price', 'Quantity Available', 'Expiry Date', 'Category', 'Drug Type'])

        # Add data rows
        products = Product.objects.all()
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


# Dashboard
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        manufacturers = Manufacturer.objects.all()
        product_types = ProductType.objects.all()

        context = {
            'products': products,
            'categories': categories,
            'manufacturers': manufacturers,
            'product_types': product_types,
        }

        return render(request, 'dashboard/overview.html', context)

# Products
class ProductsView(View):
    def get(self, request):
        form = ProductForm()
        products = Product.objects.all()
        add_generic_form = AddGenericForm()
        add_composition_form = AddCompositionForm()
        add_pack_size_form = AddPackSizeForm()
        return render(request, 'dashboard/products.html', {
            'form': form,
            'products': products,
            'add_generic_form': add_generic_form,
            'add_composition_form': add_composition_form,
            'add_pack_size_form': add_pack_size_form,
        })

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        add_generic_form = AddGenericForm(request.POST)
        add_composition_form = AddCompositionForm(request.POST)
        add_pack_size_form = AddPackSizeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard:products')

        if add_generic_form.is_valid() and 'add_generic' in request.POST:
            add_generic_form.save()

        if add_composition_form.is_valid() and 'add_composition' in request.POST:
            add_composition_form.save()

        if add_pack_size_form.is_valid() and 'add_pack_size' in request.POST:
            add_pack_size_form.save()

        products = Product.objects.all()
        return render(request, 'dashboard/products.html', {
            'form': form,
            'products': products,
            'add_generic_form': AddGenericForm(),
            'add_composition_form': AddCompositionForm(),
            'add_pack_size_form': AddPackSizeForm(),
        })



class ProductDetailsView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
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
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

class EditProductView(SuperuserRequiredMixin, View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(instance=product)
        add_generic_form = AddGenericForm()
        add_composition_form = AddCompositionForm()
        add_pack_size_form = AddPackSizeForm()
        expiry_date_value = product.expiry_date.strftime('%Y-%m-%d') if product.expiry_date else None
        return render(request, 'dashboard/edit_page/edit_product.html', {'form': form, 'add_generic_form': add_generic_form, 'add_composition_form': add_composition_form, 'add_pack_size_form': add_pack_size_form, 'expiry_date_value': expiry_date_value})

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(request.POST, request.FILES, instance=product)
        add_generic_form = AddGenericForm(request.POST)
        add_composition_form = AddCompositionForm(request.POST)
        add_pack_size_form = AddPackSizeForm(request.POST)

        if add_generic_form.is_valid() and 'add_generic' in request.POST:
            add_generic_form.save()
            return redirect('dashboard:edit_product', slug=product.slug)
            
        elif add_composition_form.is_valid() and 'add_composition' in request.POST:
            add_composition_form.save()
            return redirect('dashboard:edit_product', slug=product.slug)
            
        elif add_pack_size_form.is_valid() and 'add_pack_size' in request.POST:
            add_pack_size_form.save()
            return redirect('dashboard:edit_product', slug=product.slug)
            
        elif form.is_valid():
            product_instance = form.save(commit=False)
            new_image = form.cleaned_data.get('image')
            if new_image:
                product_instance.image = new_image
            try:
                product_instance.save()
                form.save_m2m()
                return redirect('dashboard:products')
            except ValidationError as e:
                form.add_error(None, e)

        return render(request, 'dashboard/edit_page/edit_product.html', {
            'form': form,
            'add_generic_form': add_generic_form,
            'add_composition_form': add_composition_form,
            'add_pack_size_form': add_pack_size_form,
        })


    
class DeleteProductView(SuperuserRequiredMixin, View):
    def post(self, request, slug):
        # Retrieve the product
        product = get_object_or_404(Product, slug=slug)
        
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
        form = ProductTypesForm()
        product_types = ProductType.objects.all()
        return render(request, 'dashboard/product_type.html', {'form': form, 'product_types': product_types})

    def post(self, request):
        form = ProductTypesForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # Return JSON response for success
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})  # Return JSON response for errors


@method_decorator(login_required, name='dispatch')
class EditProductTypeView(SuperuserRequiredMixin, View):
    def get(self, request, slug):
        drug_type = get_object_or_404(ProductType, slug=slug)
        form = ProductTypesForm(instance=drug_type)
        return render(request, 'dashboard/edit_page/edit_product_type.html', {'form': form})

    def post(self, request, slug):
        product_type = get_object_or_404(ProductType, slug=slug)
        form = ProductTypesForm(request.POST, instance=product_type)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product_type')
        return render(request, 'dashboard/edit_page/edit_product_type.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DeleteProductTypeView(View):
    def post(self, request, drug_type_id):
        product_type = get_object_or_404(ProductType, id=product_type)
        product_type.delete()
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


# Gallery 
@method_decorator(login_required, name='dispatch')
class GalleryListView(SuperuserRequiredMixin, View):
    template_name = 'dashboard/gallery.html'

    def get(self, request, *args, **kwargs):
        galleries = Gallery.objects.all()
        return render(request, self.template_name, {'galleries': galleries})

    def post(self, request, *args, **kwargs):
    # Process form data and save the new gallery name
        gallery_name = request.POST.get('galleryName')
        gallery_description = request.POST.get('galleryDescription')

        # Save the new gallery name to the database
        new_gallery = Gallery.objects.create(name=gallery_name, description=gallery_description)

        return redirect('dashboard:gallery_list')



@method_decorator(login_required, name='dispatch')
class UpdateGalleryView(SuperuserRequiredMixin, View):
    def get(self, request, gallery_slug):
        gallery_instance = get_object_or_404(Gallery, slug=gallery_slug)
        form = GalleryForm(instance=gallery_instance)
        image_form = ImageUploadForm()  # Create an instance of ImageUploadForm
        return render(request, 'dashboard/edit_page/edit_gallery.html', {'form': form, 'image_form': image_form, 'gallery': gallery_instance})

    def post(self, request, gallery_slug):
        gallery_instance = get_object_or_404(Gallery, slug=gallery_slug)
        form = GalleryForm(request.POST, instance=gallery_instance)
        image_form = ImageUploadForm(request.POST, request.FILES)  # Bind data from request
        if form.is_valid():
            form.save()
            if 'images_to_delete' in request.POST:
                for image_id in request.POST.getlist('images_to_delete'):
                    image = GalleryImage.objects.get(id=image_id)  # Use GalleryImage instead of Image
                    image.delete()
            if request.FILES.get('image'):  # Check if an image file has been uploaded
                image_form.instance.gallery = gallery_instance
                image_form.save()
            return redirect('dashboard:gallery_list')
        else:
            # Handle invalid form submission
            return render(request, 'dashboard/edit_page/edit_gallery.html', {'form': form, 'image_form': image_form, 'gallery': gallery_instance})

        
@method_decorator(login_required, name='dispatch')
class DeleteGalleryView(SuperuserRequiredMixin, View):
    def post(self, request, gallery_id):
        gallery = get_object_or_404(Gallery, id=gallery_id)
        gallery.delete()
        return redirect('dashboard:gallery_list')