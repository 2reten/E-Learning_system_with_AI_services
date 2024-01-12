from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'common'  # 네임스페이스 추가

urlpatterns = [
    path('login/', LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='common/logged_out.html'), name='logout'),
    path('signup/', views.signup, name='signup'),

]