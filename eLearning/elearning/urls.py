from django.contrib import admin
from django.urls import include, path
from board import views as board_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("admin/", admin.site.urls),
    path("interview/", include("interview.urls")),
    path("polls/", include("polls.urls")),
    path('board/', include("board.urls")),
    path('common/', include('common.urls')),
    path('courses/', include('courses.urls')),
    path('course-intro/<slug:slug>/', views.courseintro_detail, name='courseintro_detail'),
    path('search/', views.search, name='search'),  # Updated to use views.search
    path('about_us/', views.about_us, name='about_us'),
    path('education/', include('education.urls')),
    path('board_manage/', views.board_manage, name='board_manage'),
    path('result/', include('result.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Only add MEDIA_URL patterns in DEBUG mode