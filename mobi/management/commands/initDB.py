from mobi.models import *

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        fr = Country(name="France", continent="Europe", ECTSConversion=1)
        fr.save()

        can = Country(name="Canada", continent="Amerique du Nord", ECTSConversion=1)
        can.save()

        lyon = City(name="Lyon", country=fr)
        lyon.save()

        mtr = City(name="Montréal", country=can)
        mtr.save()

        insa = University(name="INSA", city=lyon, univ_appartment=False, latitude=45.78262952862812, longitude=4.876626999999439)
        insa.save()

        ets = University(name="ETS", city=mtr, univ_appartment=False, latitude=45.49490192138759, longitude=-73.56226838771663)
        ets.save()

        s1 = Semester(name="4A-S1")
        s1.save()
        s2 = Semester(name="4A-S2")
        s2.save()
        s3 = Semester(name="5A-S1")
        s3.save()
        s4 = Semester(name="5A-S2")
        s4.save()

        dep = ["BB", "BIM", "GCU", "GE", "GEN", "GI", "GM", "IF", "SGM", "TC"]

        tab_dep = [DepartementINSA(name=i) for i in dep]
        for i in tab_dep:
            i.save()

        argent = FinancialAid(organization="Ma Maman", name="Argent des études", approx_amount=1000, period='An')
        argent.save()
        erasmus = FinancialAid(organization="ERASMUS", name="Mobilité", approx_amount=300, period='Mensuel')
        erasmus.save()

        placesINSA = PlacesExchange(university=insa, number=10)
        placesINSA.save()
        placesINSA.semester.add(s1)
        placesINSA.department_availability.add(9)

        placesETS = PlacesDD(university=ets, number=10)
        placesETS.save()
        placesETS.department_availability.add(7)

        review = ExchangeReview(
            university=insa,
            culture=5.0,
            night_life=5.0,
            cost_of_living=5.0,
            security=5.0,
            mobility_type='E',
            univ_appartment=False,
            rent=750,
            comments="Bonjour c moi c le test",
            visa=False,
            courses_difficulty=2.0,
            courses_interest=5.0,
            student_proximity=5.0,
            certif_languages='AUCUN',
            semester="4A",
            contact=True,
            email="eric.maurincomme@insa-lyon.fr",
            department="TC",
            name="Maurincomme",
            surname="Eric",
            year=2020,
        )
        review.save()
        review.financial_aid.add(argent)
        review.save()

