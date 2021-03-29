from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import health_check, ReviewViewset, CountryViewset, UniversityViewset

# Register models to the REST router
router = routers.DefaultRouter()
router.register(r'reviewtest', ReviewViewset)
router.register(r'countrytest', CountryViewset)
router.register(r'universitytest', UniversityViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('check', health_check, name="healthcheck")
]
