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

        uni_name = request.data['name']
        uni_access = request.POST.get("access")
        uni_cultural_life_min = request.POST.get("cultural_life_min")
        uni_country = request.POST.get("country")
        uny_nightlife = request.POST.get("nightlife")
        uni_security = request.POST.get("security")
        uni_rent_max = request.POST.get("rent_max")
        uni_courses_diff = request.POST.get("courses_difficulty")
        uni_cost_living = request.POST.get("cost_living")
        uni_outside_europe = request.POST.get("outside_europe")

        queryset = queryset.filter(
            name=uni_name,
        )

        print(request.POST.get("name"))

        serializer = UniversitySerializer(queryset, many=True)
        return Response(serializer.data)



