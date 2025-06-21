from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')



def login_page(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')






65