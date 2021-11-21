from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('attendance/scanner/', views.scanner, name='Scanner'),
    path('<int:slug>/', views.showattendance, name='ShowAttendance'),
    path('generateQRCode/', views.generate_qr, name="QRCode")
]
