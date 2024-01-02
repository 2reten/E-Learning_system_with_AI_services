
from django.contrib import admin
from django.urls import include, path
from board import views
from django.conf import settings  # 추가
from django.conf.urls.static import static  # 추가
from . import views
from .views import search

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.index, name='index'),
    path("admin/", admin.site.urls),
    path("interview/", include("interview.urls")),
    path("polls/", include("polls.urls")),
    path('board/', include("board.urls")),  # 'board'를 'board/'로 수정
    path('common/', include('common.urls')),
    path('courses/', include('courses.urls')),
    path('course-intro/<slug:slug>/', views.courseintro_detail, name='courseintro_detail'),
    path('search/', search, name='search'),
    path('education/', include('education.urls')),
    path('board_manage/', views.board_manage, name='board_manage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
