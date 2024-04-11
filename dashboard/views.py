from multiprocessing import AuthenticationError
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from product.models import Manufacturer
from .models import *



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
def manufacturer(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'dashboard/manufacturer.html', {'manufacturers': manufacturers})
