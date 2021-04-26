from rest_framework.serializers import ModelSerializer
from .models import ExchangeReview, University, Country, City, DepartementINSA, FinancialAid


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


class FinancialAidSerializer(ModelSerializer):
    class Meta:
        model = FinancialAid
        fields = '__all__'


class UniversitySerializer(ModelSerializer):
    department_availability = DepartementSerializer(many=True, read_only=True)
    financial_aid = FinancialAidSerializer(many=True, read_only=True)
    reviews = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = (
            'id',
            'name',
            'department_availability',
            'cwur_rank',
            'latitude',
            'longitude',
            'website',
            'contract_type',
            'places',
            'access',
            'univ_appartment',
            'courses_difficulty',
            'courses_interest',
            'student_proximity',
            'financial_aid',
            'reviews'
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
