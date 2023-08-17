from django.urls import path
from . import views

# app_name = 'store'

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='create_user'),
    path('me/', views.LoadUserView.as_view(), name='load_user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]