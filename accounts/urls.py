from django.urls import path
from . import  views

app_name = 'accounts'
urlpatterns = [
    path('user-register/', views.user_register, name="user_register"),
    path('profile-create/', views.profile_create, name="profile_create"),
    path('user-login/', views.user_login, name="user_login"), 
    path('user-profile/', views.user_profile, name="user_profile"),
    path('become-pro/', views.become_pro, name="become_pro"),
    path('pro-status/<str>/', views.pro_status, name="pro_status"),
]
