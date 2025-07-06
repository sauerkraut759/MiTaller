from rest_framework import serializers
from core.models import Categoria, Profesor, Lugar, Taller

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
            model = Categoria
            fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
            model = Profesor
            fields = '__all__'

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
            model = Lugar
            fields = '__all__'

class TallerSerializer(serializers.ModelSerializer):
    class Meta:
            model = Taller
            fields = '__all__'