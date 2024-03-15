from rest_framework import serializers
from CrimeMapping.models import FirData

class FirDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirData
        fields = '__all__'