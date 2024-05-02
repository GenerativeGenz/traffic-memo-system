from django.contrib import admin
from django.urls import path
from admin_panel import views

urlpatterns = [
    path('', views.home),
]