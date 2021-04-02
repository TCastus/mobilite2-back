from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets
from rest_framework.status import *
from .models import *
from .serializers import ExchangeReviewSerializer, CountrySerializer, UniversitySerializer


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'ça maarche'})


@api_view(['PUT'])
def review_update(request, pk):

    try:
        review = ExchangeReview.objects.get(id=pk)
    except review.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = ExchangeReviewSerializer(review, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ReviewViewset(viewsets.ModelViewSet):
    queryset = ExchangeReview.objects.all()
    serializer_class = ExchangeReviewSerializer


class CountryViewset(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UniversityViewset(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

