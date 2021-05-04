from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import *


# Model serializers go here...


class ExchangeReviewSerializer(ModelSerializer):
    class Meta:
        model = ExchangeReview
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = ExchangeReview
        fields = (
            'comments',
            'name',
            'surname',
            'diploma_year',
        )


class DepartementSerializer(ModelSerializer):
    class Meta:
        model = DepartementINSA
        fields = ('name',)


class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = ('name',)


class FinancialAidSerializer(ModelSerializer):
    class Meta:
        model = FinancialAid
        fields = '__all__'


class UniversityBisSerializer(ModelSerializer):

    class Meta:
        model = University
        fields = (
            'id',
            'name'
        )


class CitySerializer(ModelSerializer):
    universities = UniversityBisSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ('name', 'universities')


class CountrySerializer(ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ('id', 'name', 'cities')


class PlacesExchangeSerializer(ModelSerializer):
    department_availability = DepartementSerializer(many=True, read_only=True)
    semester = SemesterSerializer(many=True, read_only=True)

    class Meta:
        model = PlacesExchange
        fields = ('number', 'department_availability', 'semester')


class PlacesDDSerializer(ModelSerializer):
    department_availability = DepartementSerializer(many=True, read_only=True)

    class Meta:
        model = PlacesDD
        fields = ('number', 'department_availability')


class UniversitySerializer(ModelSerializer):
    department_availability = DepartementSerializer(many=True, read_only=True)
    financial_aid = FinancialAidSerializer(many=True, read_only=True)
    reviews = CommentSerializer(many=True, read_only=True)
    placesExchange = PlacesExchangeSerializer(many=True, read_only=True)
    placesDD = PlacesDDSerializer(many=True, read_only=True)
    city_name = ReadOnlyField()
    country_name = ReadOnlyField()

    class Meta:
        model = University
        fields = (
            'id',
            'name',
            'city_name',
            'country_name',
            'department_availability',
            'cwur_rank',
            'latitude',
            'longitude',
            'website',
            'access',
            'placesExchange',
            'placesDD',
            'univ_appartment',
            'courses_difficulty',
            'courses_interest',
            'student_proximity',
            'financial_aid',
            'reviews'
        )




