from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('marks/upload/', views.upload_marks, name="UploadMarks"),
    path('marks/<int:slug>/', views.view_marks, name="showTable")
]
