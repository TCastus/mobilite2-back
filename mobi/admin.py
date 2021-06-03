from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from mobi.models import University, ExchangeReview, City, DepartementINSA, Country, Semester, FinancialAid, PlacesExchange, PlacesDD

admin.site.register(ExchangeReview)
admin.site.register(DepartementINSA)


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    pass


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    pass


@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Semester)
admin.site.register(FinancialAid)
admin.site.register(PlacesExchange)
admin.site.register(PlacesDD)