from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .serializers import ExchangeReviewSerializer, CountrySerializer, UniversitySerializer, UniversityShortSerializer


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'ça maarche'})


@api_view(['GET'])
def homepage(request):
    return render(request, 'homepage.html')

class ReviewViewset(viewsets.ModelViewSet):
    queryset = ExchangeReview.objects.all()
    serializer_class = ExchangeReviewSerializer


class CountryViewset(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UniversityViewset(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class UniversityShortViewset(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversityShortSerializer
