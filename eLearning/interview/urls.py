from django.urls import path
from . import views
from .views import interview_home
from .views import pre_interview


urlpatterns = [
    path('', interview_home, name='interview_home'),
    path('start_interview/', views.start_interview, name='start_interview'),  # URL 패턴 추가
    path('analyze/', views.analyze_emotion, name='analyze_emotion'),
    path('uploads/', views.upload_audio, name='upload_audio'),
    path('pre_interview/', pre_interview, name='pre_interview'),
    path('media/', views.upload_image, name='upload_image'),
]
