from rest_framework import serializers

from storeapp.models import Marks, Moto_models, Moto_type, City, Motorcycle
from newsapp.models import News


class MarkSerializer(serializers.ModelSerializer):
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


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class MotorcycleSerializer(serializers.ModelSerializer):
    displacement = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    transmission = serializers.StringRelatedField()
    mark_info = serializers.StringRelatedField()
    model_info = serializers.StringRelatedField()
    moto_type = serializers.StringRelatedField()
    city = serializers.StringRelatedField()

    class Meta:
        model = Motorcycle
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = News
        fields = '__all__'