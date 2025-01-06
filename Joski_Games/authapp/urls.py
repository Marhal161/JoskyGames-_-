from django.urls import path
from .views.RegisterView import RegisterView, RegisterFView
from .views.LoginView import LoginView
from .views.LogoutView import LogoutView
from .views.LoginFormView import LoginFView

urlpatterns = [
    path('register/', RegisterFView.as_view(), name='register_form'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('login/', LoginFView.as_view(), name='login_form'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]