from rest_framework import serializers

from .models import RateModel


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RateModel
        fields = ("result",)
