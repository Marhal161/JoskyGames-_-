from django.urls import path
from .views import MainFView


urlpatterns = [
    path('/', MainFView.as_view(), name='main'),

]