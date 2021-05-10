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
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


@api_view(['POST'])
def search(request):
    if request.method == 'POST':

        queryset = University.objects.all()




        #uni_rent_max = request.data['rent_max']

        #uni_cost_living = request.data['cost_living']


        if 'name' in request.data:
            uni_name = request.data['name']
            queryset = queryset.filter(name__iexact=uni_name)
        if 'access' in request.data:
            uni_access = request.data['access']
            queryset = queryset.filter(access=uni_access)
        if 'country' in request.data:
            uni_country = request.data['country']
            queryset = queryset.filter(city__country__name__icontains=uni_country)
        if 'nightlife' in request.data:
            uni_nightlife = request.data['nightlife']
            queryset = queryset.filter(city__night_life_average_grade__gte=uni_nightlife)
        if 'courses_diff' in request.data:
            uni_courses_diff = request.data['courses_difficulty']
            queryset = queryset.filter(courses_difficulty__lte=uni_courses_diff)
        if 'security' in request.data:
            uni_security = request.data['security']
            queryset = queryset.filter(city__security_average_grade__gte=uni_security)
        if 'cultural_life_min' in request.data:
            uni_cultural_life_min = request.data['cultural_life_min']
            queryset = queryset.filter(city__cultural_life_average_grade__gte=uni_cultural_life_min)
        if 'outside_europe' in request.data:
            uni_outside_europe = request.data['outside_europe']
            if uni_outside_europe == 'True':
                queryset = queryset.exclude(city__country__continent="Europe")
            else:
                queryset = queryset.filter(city__country__continent="Europe")


        #Attenton si la key existe mais est reliée a rien
        #Dans les models, changer la rent de City à University
        #On s'en branle du loyer dans la ville. On veut le loyer des logements uniersitaires.

        serializer = UniversitySerializer(queryset, many=True)

        return Response(serializer.data)



