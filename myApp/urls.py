from django.urls import path
from . import views


urlpatterns = [
    path('marks/upload/', views.upload_marks, name="UploadMarks"),
    path('marks/<int:slug>/', views.view_marks, name="ShowTable")
]
