from rest_framework.serializers import ModelSerializer
from .models import ExchangeReview

# Model serializers go here...


class ExchangeReviewSerializer(ModelSerializer):
    class Meta:
        model = ExchangeReview
        fields = '__all__'
