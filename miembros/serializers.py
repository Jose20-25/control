from rest_framework import serializers
from .models import Miembro, Familia

class FamiliaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Familia
        fields = '__all__'

class MiembroSerializer(serializers.ModelSerializer):
    familia = FamiliaSerializer(many=True, read_only=True)

    class Meta:
        model = Miembro
        fields = '__all__'
