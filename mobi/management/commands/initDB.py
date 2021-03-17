from mobi.models import *

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        a = Country(name="France", continent="Europe", ECTSConversion=1)
        a.save()

        b = City(name="Lyon", country=a)
        b.save()

        c = University(name="INSA", contract_type="E", city=b, univ_appartment=False)
        c.save()


