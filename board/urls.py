from django.urls import path
from . import views
from board.views import question_vote



app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/vote/<int:question_id>/', views.question_vote, name='question_vote'),
    path('answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),
    path('board_manage/', views.board_manage, name='board_manage'),
    path('board/', views.board_list, name='board_list'),  # 게시판 목록
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),  # 각 게시판 상세 페이지
    ]
