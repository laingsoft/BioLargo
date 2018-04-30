from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'frontpage/index.html')

def contactus(request):
    return render(request, 'frontpage/contactus.html')

def pricing(request):
    return render(request, 'frontpage/pricing.html')

def support(request):
    return render(request, 'frontpage/support.html')

def features(request):
    return render(request, 'frontpage/features.html')


