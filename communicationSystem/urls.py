from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('createGroup/', views.create_group, name='createGroup'),
    path('group/<str:slug>/', views.get_group, name='getGroup'),
    path('group/submission/<str:slug1>/', views.submit_assign, name='submitAssign'),
    path('assignmentsSubmitted/<str:slug>/', views.display_submitted_assign, name='serveFile')
]
