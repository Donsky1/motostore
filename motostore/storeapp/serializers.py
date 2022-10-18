from rest_framework import serializers

from .models import Marks, Moto_models, Moto_type


class MarkSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='marks-detail')

    class Meta:
        model = Marks
        fields = '__all__'


class MotorcycleModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto_models
        fields = '__all__'


class MotorcycleTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto_type
        fields = '__all__'
