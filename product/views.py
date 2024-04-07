from django.shortcuts import render

# Create your views here.
def anti_infective(request):
    return render(request, 'products/anti_infective.html')