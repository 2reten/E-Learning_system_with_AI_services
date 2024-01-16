# elearning_project/urls.py# courses/urls.py
from django.urls import path
from .views import course_list
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import course_detail, course_list
from .views import course_add, course_edit
from .views import dashboard


app_name = 'courses'

urlpatterns = [
    path('', course_list, name='course_list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/',views.course_detail, name='course_detail'),
    path('add/', course_add, name='course_add'),
    path('<int:pk>/edit/', course_edit, name='course_edit'),
    path('dashboard/', dashboard, name='dashboard'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),

]

