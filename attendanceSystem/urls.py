from django.urls import path
from . import views


urlpatterns = [
    path('<int:slug>/', views.show_attendance, name='ShowAttendance'),
    path('generateQRCode/', views.generate_qr, name="QRCode"),
    path('attendance/scanner/', views.scanner, name='Scanner'),
    path('postResults/', views.scanner_results, name="QRResults")
]
