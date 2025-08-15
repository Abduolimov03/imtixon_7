from rest_framework import serializers
from .models import Kompyuter

class KompyuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kompyuter
        fields = '__all__'