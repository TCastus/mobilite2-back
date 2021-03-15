from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets
from .models import ExchangeReview
from .serializers import ExchangeReviewSerializer


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'ça maarche'})


class ReviewViewset(viewsets.ModelViewSet):
    queryset = ExchangeReview.objects.all()
    serializer_class = ExchangeReviewSerializer


