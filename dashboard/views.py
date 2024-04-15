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
        return render(request, 'dashboard/dashboard.html')

# Products
@method_decorator(login_required, name='dispatch')
class ProductsView(View):
    def get(self, request):
        return render(request, 'dashboard/products.html')


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
class EditCategoryView(View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        form = CategoryForm(instance=category)
        return render(request, 'dashboard/edit_page/edit_category.html', {'form': form})

    def post(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category_list')
        return render(request, 'dashboard/edit_page/edit_category.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DeleteCategoryView(View):
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
class EditManufacturerView(View):
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
class DeleteManufacturerView(View):
    def post(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
        manufacturer.delete()
        return redirect('dashboard:manufacturer')

# @method_decorator(login_required, name='dispatch')
# class AddManufacturerView(View):
#     def get(self, request):
#         form = ManufacturerForm()
#         return render(request, 'dashboard/add_page/add_manufacturer.html', {'form': form})

#     def post(self, request):
#         form = ManufacturerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard:manufacturer')
#         return render(request, 'dashboard/add_page/add_manufacturer.html', {'form': form})


# Product type
@method_decorator(login_required, name='dispatch')
class ProductTypeView(View):
    def get(self, request):
        form = DrugTypeForm()
        drug_types = DrugType.objects.all()
        return render(request, 'dashboard/product_type.html', {'form': form, 'drug_types': drug_types})

    def post(self, request):
        form = DrugTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product_type')
        drug_types = DrugType.objects.all()
        return render(request, 'dashboard/product_type.html', {'form': form, 'drug_types': drug_types})


@method_decorator(login_required, name='dispatch')
class EditProductTypeView(View):
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
        news_items = New.objects.all().order_by('-updated_at')
        return render(request, 'dashboard/news.html', {'news_items': news_items})

@method_decorator(login_required, name='dispatch')
class AddNewsView(View):
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
class EditNewsView(View):
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
class DeleteNewsView(View):
    def post(self, request, new_id):
        new = get_object_or_404(New, id=new_id)
        new.delete()
        return redirect('dashboard:news')