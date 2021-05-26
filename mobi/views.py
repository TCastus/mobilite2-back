import requests


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .models import *
from .serializers import ExchangeReviewSerializer, CountrySerializer, UniversitySerializer
from django.http import HttpResponse
from mobi2_app import settings
from .serializers import ExchangeReviewSerializer, CountrySerializer, UniversitySerializer, UniversityShortSerializer


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'ça maarche'})


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