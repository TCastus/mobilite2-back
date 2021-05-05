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
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

