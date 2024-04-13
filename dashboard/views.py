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



def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or any other page after login
            return redirect("dashboard:dashboard")
        else:
            # Handle invalid login credentials
            return render(
                request,
                "dashboard/sign_in.html",
                {"error_message": "Invalid username or password"},
            )
    return render(request, "dashboard/sign_in.html")


def logout_view(request):
    logout(request)
    return redirect('dashboard:sign_in')



def dashboard_base(request):
    return render(request, 'dashboard/dashboard_base.html')

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("dashboard:sign_in")
    return render(request, 'dashboard/dashboard.html')

@login_required
def products(request):
    return render(request, 'dashboard/products.html')


# category
@login_required
def category(request):
    category = Category.objects.all()
    return render(request, 'dashboard/category.html', {'categories': category})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category') 
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/edit_page/edit_category.html', {'form': form})

@login_required
def delete_category(request, category_id):
    if request.method == 'POST':
        # Retrieve the category object
        category = Category.objects.get(id=category_id)
        # Delete the category
        category.delete()
        # Redirect to a page after successful deletion
        return redirect('dashboard:category')
    else:
        pass
    
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category')  # Redirect to the category list page
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_page/add_category.html', {'form': form})



# Manufacturer
@login_required
def manufacturer(request):
    if request.method == 'GET' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # AJAX request to retrieve manufacturer data
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
        # Regular GET request to render the page
        manufacturers = Manufacturer.objects.all()
        return render(request, 'dashboard/manufacturer.html', {'manufacturers': manufacturers})


@login_required
def edit_manufacturer(request, manufacturer_id):
    # Retrieve the manufacturer object or return a 404 error if not found
    manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
    
    if request.method == 'POST':
        # If the form is submitted
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            # Save the form data to update the manufacturer object
            form.save()
            return redirect('dashboard:manufacturer')  # Redirect to the manufacturer list page
    else:
        # If it's a GET request, prepopulate the form with the manufacturer's current data
        form = ManufacturerForm(instance=manufacturer)
    
    return render(request, 'dashboard/edit_page/edit_manufacturer.html', {'form': form})

def delete_manufacturer(request, manufacturer_id):
    if request.method == 'POST':
        # Retrieve the manufacturer object
        manufacturer = Manufacturer.objects.get(id=manufacturer_id)
        # Delete the manufacturer
        manufacturer.delete()
        # Redirect to a page after successful deletion
        return redirect('dashboard:manufacturer')
    else:
        pass

@login_required
def add_manufacturer(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manufacturer')  # Redirect to the category list page
    else:
        form = ManufacturerForm()  
    return render(request, 'dashboard/add_page/add_manufacturer.html', {'form': form})

# Product type 
@login_required
def product_type(request):
    # Assuming you want to pass all drug types to the template
    drug_types = DrugType.objects.all()
    return render(request, 'dashboard/product_type.html', {'drug_types': drug_types})


@login_required
def add_product_type(request):
    if request.method == 'POST':
        form = DrugTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product_type') 
    else:
        form = DrugTypeForm()
    return render(request, 'dashboard/add_page/add_product_type.html', {'form': form})

@login_required
def edit_product_type(request, drug_type_id):
    drug_type = get_object_or_404(DrugType, id=drug_type_id)
    if request.method == 'POST':
        form = DrugTypeForm(request.POST, instance=drug_type)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product_type')
    else:
        form = DrugTypeForm(instance=drug_type)
    return render(request, 'dashboard/edit_page/edit_product_type.html', {'form': form})

@login_required
def delete_product_type(request, drug_type_id):
    drug_type = get_object_or_404(DrugType, id=drug_type_id)
    if request.method == 'POST':
        drug_type.delete()
        return redirect('dashboard:product_type')
    return render(request, 'dashboard/delete_product_type.html', {'drug_type': drug_type})

# News
def news(request):
    news_items = New.objects.all().order_by('-updated_at')
    return render(request, 'dashboard/news.html', {'news_items': news_items})



@login_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_instance = form.save(commit=False)
            if 'publishCheckbox' in request.POST:
                news_instance.is_published = True
            news_instance.save()
            return redirect('dashboard:news')
    else:
        form = NewsForm()
    return render(request, 'dashboard/add_page/add_news.html', {'form': form})



@login_required
def edit_news(request, new_id):
    new = get_object_or_404(New, id=new_id)
    if request.method == 'POST':
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
    else:
        form = NewsForm(instance=new)
    return render(request, 'dashboard/edit_page/edit_news.html', {'form': form, 'new': new})





def update_history(request, new_id):
    new = get_object_or_404(New, id=new_id)
    update_history_entries = new.updatehistory_set.all().order_by('-update_time')
    return render(request, 'dashboard/history/update_new_history.html', {'new': new, 'update_history_entries': update_history_entries})


@login_required
def delete_news(request, new_id):
    new = get_object_or_404(New, id=new_id)
    if request.method == 'POST':
        new.delete()
        return redirect('dashboard:news')
    else:
        pass
