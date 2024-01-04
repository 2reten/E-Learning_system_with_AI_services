from django.urls import path
from . views import interview_home, start_interview
from . import views

urlpatterns = [
    path('', interview_home, name='interview_home'),
    path('start_interview/', views.start_interview, name='start_interview'),  # URL 패턴 추가
]
