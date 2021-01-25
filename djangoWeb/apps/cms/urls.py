from rest_framework.routers import DefaultRouter
from .views import LoginView
from django.urls import path


app_name = 'cms'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    # path('register/', RegisterView.as_view(), name='register'),
]
