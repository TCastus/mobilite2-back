from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import *


# Model serializers go here...

class CommentSerializer(ModelSerializer):
    class Meta:
        model = ExchangeReview
        fields = (
            'comments',
            'name',
            'surname',
            'year',
            'semester',
            'datetime',
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


class ExchangeReviewSerializer(ModelSerializer):
    financial_aid = FinancialAidSerializer(many=True, read_only=True)

    class Meta:
        model = ExchangeReview
        fields = (
            'datetime',
            'name',
            'surname',
            'contact',
            'email',
            'department',
            'university',
            'mobility_type',
            'semester',
            'year',
            'culture',
            'night_life',
            'cost_of_living',
            'security',
            'courses_difficulty',
            'courses_interest',
            'student_proximity',
            'univ_appartment',
            'rent',
            'visa',
            'certif_languages',
            'financial_aid',
            'comments'
        )


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


class UniversityShortSerializer(ModelSerializer):
    city_name = ReadOnlyField()
    country_name = ReadOnlyField()
    placesExchange = PlacesExchangeSerializer(many=True, read_only=True)
    placesDD = PlacesDDSerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = (
            'id',
            'name',
            'city_name',
            'country_name',
            'placesExchange',
            'placesDD'
        )


class UniversitySerializer(ModelSerializer):
    financial_aid = FinancialAidSerializer(many=True, read_only=True)
    reviews = CommentSerializer(many=True, read_only=True)
    placesExchange = PlacesExchangeSerializer(many=True, read_only=True)
    placesDD = PlacesDDSerializer(many=True, read_only=True)
    city_name = ReadOnlyField()
    country_name = ReadOnlyField()
    courses_difficulty = ReadOnlyField()
    courses_interest = ReadOnlyField()
    student_proximity = ReadOnlyField()
    review_number = ReadOnlyField()
    culture = ReadOnlyField()
    night_life = ReadOnlyField()
    cost_of_living = ReadOnlyField()
    security = ReadOnlyField()
    rent = ReadOnlyField()

    class Meta:
        model = University
        fields = (
            'id',
            'name',
            'city_name',
            'country_name',
            'cwur_rank',
            'latitude',
            'longitude',
            'website',
            'access',
            'placesExchange',
            'placesDD',
            'univ_appartment',
            'review_number',
            'courses_difficulty',
            'courses_interest',
            'student_proximity',
            'culture',
            'night_life',
            'cost_of_living',
            'security',
            'rent',
            'financial_aid',
            'reviews'
        )






