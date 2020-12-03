from rest_framework import serializers

from app.web.models import Good


class ListGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ['id', 'name', 'status', 'price', 'created_at', 'updated_at', 'is_deleted']
