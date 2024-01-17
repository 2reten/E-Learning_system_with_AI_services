from django.urls import path
from .views import lecture_programs_list, lecture_detail, education_home  # Ensure correct import
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ... your other url patterns ...
    path('', education_home, name='education_home'),
    path('education/', lecture_programs_list, name='lecture_programs_list'),
    path('programs/<int:pk>/', lecture_detail, name='lecture_detail'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
