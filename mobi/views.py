import requests


from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .models import *
from django.http import HttpResponse
from mobi2_app import settings
from .serializers import ExchangeReviewSerializer, CountrySerializer, UniversitySerializer, UniversityShortSerializer


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'ça maarche'})


@api_view(['GET'])
def homepage(request):
    return render(request, 'homepage.html')


class ReviewViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ExchangeReview.objects.all()
    serializer_class = ExchangeReviewSerializer

    def post(self, request, *args, **kwargs):
        super(ReviewViewset, self).create()

        if not validate_captcha(request.POST['h-captcha-response']):
            return HttpResponse('<h1>Error 429<h1>')


class CountryViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UniversityViewset(viewsets.ReadOnlyModelViewSet):
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


class UniversityShortViewset(viewsets.ReadOnlyModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversityShortSerializer


def validate_captcha(token):
    """
    Verifies the HCaptcha attached to the form
    Read the docs for more information : https://docs.hcaptcha.com/

    :param token: token provided by the form
    :return: True if HCaptcha validates the captcha
    """

    params = {
        "secret": settings.HCAPTCHA_PRIVATE_KEY,
        "response": token
    }

    captcha_result = requests.post("https://hcaptcha.com/siteverify", params)
    return captcha_result.json()['success']