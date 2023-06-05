"""
URL configuration for user_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include
from managementapi import views

# from managementapi.views import ChangePasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/post/', views.UserPost.as_view(), name='user_post'),
    path('user/list/', views.UserList.as_view(), name='user_list'),
    path('user/retrieve/<int:pk>/', views.UserDetailView.as_view(), name="user_retrieve"),
    path('user/update/<int:pk>/', views.UserUpdate.as_view(), name="user_update"),
    path('user/delete/<int:pk>/', views.UserDetailView.as_view(), name="user_delete"),
    path('user/login/', views.LoginView.as_view()),
    path('user/logout/', views.LogoutView.as_view()),
    path('user/activation_link/<uidb64>/<token>/', views.activate, name='user_activate'),
    path('user/accountactivation/', views.AccountActivation.as_view(), name='user_accountactivation'),
    path('user/forget/', views.ForgetPassword.as_view(), name='user_forget'),
    path('user/reset/<int:user_id>/<str:token>/', views.ChangePassword.as_view(), name='user_reset'),


]
