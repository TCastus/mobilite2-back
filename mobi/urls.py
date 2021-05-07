from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import health_check, ReviewViewset, CountryViewset, UniversityViewset, search

# Register models to the REST router
router = routers.DefaultRouter()
router.register(r'review', ReviewViewset)
router.register(r'country', CountryViewset)
router.register(r'university', UniversityViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('check', health_check, name="healthcheck"),
    path('search', search, name='search')
]
