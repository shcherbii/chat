from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

# app_name = "users"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='chat/index.html'), name='logout'),
]
