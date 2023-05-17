from rest_framework import serializers
from .models import NdviModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdviModel
        fields = '__all__'
