from django.contrib import admin

# Register your models here.
from mobi.models import University, ExchangeReview, City, DepartementINSA, Country

admin.site.register(University)
admin.site.register(ExchangeReview)
admin.site.register(City)
admin.site.register(DepartementINSA)
admin.site.register(Country)
