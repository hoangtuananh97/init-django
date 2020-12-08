from rest_framework import serializers

from app.utils import error_json_render
from app.web.models import Good


class CommonGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ['id', 'name', 'status', 'price', 'created_at', 'updated_at', 'is_deleted']


class CreateGoodSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=True)

    class Meta:
        model = Good
        fields = ['id', 'name', 'status', 'price', 'created_at', 'updated_at', 'is_deleted']

    def validate(self, attrs):
        name = attrs['name']
        price = attrs['price']
        if not name and not price:
            raise error_json_render.BadRequestException
        return attrs

    def create(self, validated_data):
        try:
            return Good.objects.create(
                name=validated_data.get('name'),
                status=0,
                price=validated_data.get('price')
            )
        except Exception as e:
            raise error_json_render.BadRequestException
