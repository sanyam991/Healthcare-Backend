"""
URL configuration for healthcare_backend project.
"""
from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
def home(request):
     return render(request, "home.html")
def register_page(request):
    return render(request, "register.html")


def login_page(request):
    return render(request, "login.html")
urlpatterns = [
    path("", home, name="home"), 
    path("register-page/", register_page, name="register_page"),
    path("login/", login_page, name="login_page"),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/mappings/', include('mappings.urls')),
]
