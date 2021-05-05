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

