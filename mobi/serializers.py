from rest_framework.serializers import ModelSerializer, RelatedField, SlugRelatedField
from .models import ExchangeReview, University, Country, City

# Model serializers go here...


class ExchangeReviewSerializer(ModelSerializer):
    class Meta:
        model = ExchangeReview
        fields = '__all__'


class UniversitySerializer(ModelSerializer):

    class Meta:
        model = University
        fields = ('name', 'department_availability')


class CitySerializer(ModelSerializer):
    universities = UniversitySerializer(many=True)

    class Meta:
        model = City
        fields = ('name', 'universities')


class CountrySerializer(ModelSerializer):
    cities = CitySerializer(many=True)

    class Meta:
        model = Country
        fields = ('name', 'cities')
