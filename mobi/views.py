from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters
from .models import *
from .serializers import ExchangeReviewSerializer, CountrySerializer, UniversitySerializer


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'ça maarche'})


class ReviewViewset(viewsets.ModelViewSet):
    queryset = ExchangeReview.objects.all()
    serializer_class = ExchangeReviewSerializer


class CountryViewset(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UniversityViewset(viewsets.ModelViewSet):
    search_fields = ('name', 'city__name', 'city__country__name', )
    ordering_filters = ('cwur_rank',
                        'courses_interest',
                        'courses_difficulty',
                        'student_proximity',
                        'name', )
    filter_backends = (filters.SearchFilter)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


@api_view(['POST'])
def search(request):
    if request.method == 'POST':

        queryset = University.objects.all()

        if 'name' in request.data:
            uni_name = request.data['name']
            queryset = queryset.filter(name__icontains=uni_name)
        if 'access' in request.data:
            uni_access = request.data['access']
            queryset = queryset.filter(access=uni_access)
        if 'country' in request.data:
            uni_country = request.data['country']
            queryset = queryset.filter(city__country__name__icontains=uni_country)
        if 'nightlife_min' in request.data:
            uni_nightlife_min = request.data['nightlife_min']
            queryset = queryset.filter(city__night_life_average_grade__gte=uni_nightlife_min)
        if 'courses_diff' in request.data:
            uni_courses_diff = request.data['courses_difficulty']
            queryset = queryset.filter(courses_difficulty__lte=uni_courses_diff)
        if 'cultural_min' in request.data:
            uni_cultural_min = request.data['cultural_min']
            queryset = queryset.filter(city__cultural_life_average_grade__gte=uni_cultural_min)
        if 'outside_europe' in request.data:
            uni_outside_europe = request.data['outside_europe']
            if uni_outside_europe == 'True':
                queryset = queryset.exclude(city__country__continent="Europe")
            else:
                queryset = queryset.filter(city__country__continent="Europe")
        if 'department_availability' in request.data:
            uni_department_availability = request.data['department_availability']
            queryset = queryset.filter(department_availability__iexact=uni_department_availability)
        if 'cost_living_grade_min' in request.data:
            uni_cost_living_grade_min = request.data['cost_living_grade_min']
            queryset = queryset.filter(city__cost_of_living_average_grade__gte=uni_cost_living_grade_min)

        serializer = UniversitySerializer(queryset, many=True)

        return Response(serializer.data)
