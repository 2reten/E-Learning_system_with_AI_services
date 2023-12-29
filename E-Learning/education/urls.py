from django.urls import path
from . import views

urlpatterns = [
    path('', views.lecture_programs_list, name='programs'),
    path('program/<int:pk>/', views.lecture_program_detail, name='program_detail'),
]
