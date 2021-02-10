from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "pages/homepage.html")

def about(request):
    return render(request, "pages/aboutpage.html")
