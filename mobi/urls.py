from django.contrib import admin
from django.urls import path, include
from .views import healthcheck

urlpatterns = [
    path('check', healthcheck, name="healthcheck")
]
