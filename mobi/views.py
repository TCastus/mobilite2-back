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
        if not validate_captcha(request.POST['h-captcha-response']):
            return HttpResponse(status=401)
        super(ReviewViewset, self).create(request, *args, **kwargs)


class CountryViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UniversityViewset(viewsets.ReadOnlyModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


@api_view(['POST'])
def search(request):
    if request.method == 'POST':
        print(request.data)
        queryset = University.objects.all()

        if 'name' in request.data:
            uni_name = request.data['name']
            queryset = queryset.filter(name__icontains=uni_name)
        if 'outside_europe' in request.data:
            uni_outside_europe = request.data['outside_europe']
            if uni_outside_europe == 'true':
                queryset = queryset.filter(city__country__continent="Europe")
        if 'access' in request.data and request.data['access'] and request.data['access'] != "Indifférent":
            uni_access = request.data['access']
            queryset = queryset.filter(access=uni_access)
        if 'country' in request.data:
            uni_country = request.data['country']
            queryset = queryset.filter(city__country__name__icontains=uni_country)
        if 'nightlife_min' in request.data and request.data['nightlife_min'] > 0:
            uni_nightlife_min = request.data['nightlife_min']
            id_univ = [university.id for university in queryset
                       if university.night_life()['night_life__avg'] >= uni_nightlife_min]
            queryset = queryset.filter(id__in=id_univ)
        if 'course_difficulty' in request.data and request.data['course_difficulty'] > 0:
            uni_courses_diff = request.data['course_difficulty']
            id_univ = [university.id for university in queryset
                       if university.courses_difficulty()['courses_difficulty__avg'] >= uni_courses_diff]
            queryset = queryset.filter(id__in=id_univ)
        if 'uni_cultural_min' in request.data and request.data['uni_cultural_min'] > 0:
            uni_cultural_min = request.data['uni_cultural_min']
            id_univ = [university.id for university in queryset
                       if university.culture()['culture__avg'] >= uni_cultural_min]
            queryset = queryset.filter(id__in=id_univ)
        if 'department_availability' in request.data and request.data['department_availability'] != 'all':
            dep = request.data['department_availability']
            id_dep_available = [university.id for university in queryset if dep in university.department()]
            queryset = queryset.filter(id__in=id_dep_available)
        if 'cost_living_grade_min' in request.data and request.data['cost_living_grade_min'] > 0:
            uni_cost_living_grade_min = request.data['cost_living_grade_min']
            id_univ = [university.id for university in queryset if university.cost_of_living()['cost_of_living__avg'] >= uni_cost_living_grade_min]
            queryset = queryset.filter(id__in=id_univ)

        serializer = UniversityShortSerializer(queryset, many=True)
        print(len(queryset))
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
