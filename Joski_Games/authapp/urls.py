from django.urls import path
from .views.RegisterView import RegisterView
from .views.LoginView import LoginView
from .views.LogoutView import LogoutView
from .views.AuthFormView import AuthView

urlpatterns = [
    path('authorized/', AuthView.as_view(), name='auth'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]