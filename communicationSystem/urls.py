from django.urls import path
from . import views


urlpatterns = [
    path('createGroup/', views.create_group, name='CreateGroup'),
    path('group/<str:slug>/', views.get_group, name='GetGroup'),
    path('group/<str:slug>/createAssign', views.create_assignment, name='CreateAssignment'),
    path("group/<str:slug>/assignment/<str:slug1>", views.view_assignments, name="Submissions"),
    path('group/<str:slug>/submission/<str:slug1>', views.submit_assign, name='SubmitAssign'),
    path('assignmentsSubmitted/<int:slug>/', views.display_submitted_assign, name='ServeFile')
]
