from rest_framework import serializers

from app.utils import error_json_render
from app.utils.fields import Base64ImageField
from app.utils.utils import field_representation
from app.web.models import Good, ImageGood


class CommonGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ['id', 'name', 'status', 'price', 'created_at', 'updated_at', 'is_deleted']

    def to_representation(self, instance):
        data = super(CommonGoodSerializer, self).to_representation(instance)
        fields = ['name']
        data_new = field_representation(instance, fields)
        if data_new:
            data.update(data_new)
        return data


class CreateImageGood(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)
    good_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ImageGood
        fields = ('image', 'good_id')


class ListImageGood(serializers.ModelSerializer):
    class Meta:
        model = ImageGood
        fields = '__all__'


class CreateGoodSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=True)
    images = serializers.ListSerializer(child=CreateImageGood(), required=False)

    class Meta:
        model = Good
        fields = ['id', 'name', 'status', 'price', 'created_at', 'updated_at', 'is_deleted', 'images']

    def validate(self, attrs):
        name = attrs['name']
        price = attrs['price']
        if not name and not price:
            raise error_json_render.BadRequestException
        return attrs

    def create(self, validated_data):
        try:
            good = Good.objects.create(
                name=validated_data.get('name'),
                status=0,
                price=validated_data.get('price')
            )

            ImageGood.objects.bulk_create(
                [ImageGood(good=good, image=image['image']) for image in validated_data['images']]
            )

            return good

        except Exception as e:
            raise error_json_render.BadRequestException

    def to_representation(self, instance):
        response = super(CreateGoodSerializer, self).to_representation(instance)
        response['images'] = ListImageGood(ImageGood.objects.filter(good_id=instance.id), many=True).data
        return response
