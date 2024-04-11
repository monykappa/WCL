from multiprocessing import AuthenticationError
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import *
from product.models import *
from .models import *


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
    
    return render(request, 'dashboard/edit_manufacturer.html', {'form': form})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category') 
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/edit_category.html', {'form': form})
    


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

@login_required
def category(request):
    # object all
    category = Category.objects.all()
    
    return render(request, 'dashboard/category.html', {'categories': category})




# def get_manufacturer_data(request):
#     manufacturer_id = request.GET.get('manufacturer_id')
#     try:
#         manufacturer = Manufacturer.objects.get(id=manufacturer_id)
#         data = {
#             'name': manufacturer.name,
#             'country': manufacturer.country.name,  # Use .name to get the country name
#             'description': manufacturer.description,
#         }
#         return JsonResponse(data)
#     except Manufacturer.DoesNotExist:
#         return JsonResponse({'error': 'Manufacturer not found'}, status=404)


# def update_manufacturer(request):
#     if request.method == 'POST' and request.is_ajax():
#         # Get form data
#         manufacturer_id = request.POST.get('id')
#         name = request.POST.get('name')
#         country = request.POST.get('country')
#         description = request.POST.get('description')
        
#         try:
#             # Get the manufacturer object
#             manufacturer = Manufacturer.objects.get(id=manufacturer_id)
#             # Update manufacturer data
#             manufacturer.name = name
#             manufacturer.country = country
#             manufacturer.description = description
#             manufacturer.save()  # Save changes to the database
#             return JsonResponse({'success': True})
#         except Manufacturer.DoesNotExist:
#             return JsonResponse({'error': 'Manufacturer not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)
        
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
