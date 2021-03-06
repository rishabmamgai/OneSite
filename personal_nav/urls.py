"""personal_nav URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign_in, name='Main'),
    path('home/', views.home_staff, name='HomeStaff'),
    path('home_student/', views.home_student, name='HomeStudent'),
    path('home/search/', views.search, name="Search"),
    path('home/<str:slug1>/<str:slug2>/', views.branch_n_year, name='SearchResults'),
    path('signIn/', views.sign_in, name='SignIn'),
    path('signUp/', views.sign_up, name='SignUp'),
    path('signOut/', views.sign_out, name='SignOut'),
    path('marksApp/', include('myApp.urls')),
    path('attendanceSystem/', include('attendanceSystem.urls')),
    path('communicationSystem/', include('communicationSystem.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
