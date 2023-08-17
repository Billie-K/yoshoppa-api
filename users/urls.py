"""Defines URL patterns for users"""

from django.urls import path, include
from . import views


app_name = 'users'
urlpatterns = [
    #Register
    path('register', views.register_request, name='register'),

    #Login
    path('login/', views.login_request, name='login'),

    #Logout
    path('logout/', views.logout_request, name='logout'),

    #Reset Password
    path('password_reset', views.password_reset_request, name='password_reset'),
]