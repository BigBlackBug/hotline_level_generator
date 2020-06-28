from django.conf import settings
from rest_framework import serializers

from .models import HotlineUser, Level


class LevelSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format=settings.DATETIME_FORMAT,
                                           read_only=True)
    image = serializers.ImageField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    level_config = serializers.JSONField(required=False, allow_null=True)

    def create(self, validated_data):
        """
        name, level_config, is_public
        :param validated_data:
        :return:
        """
        user = self.context['request'].user
        level = Level.objects.create(**validated_data, creator=user)
        return level

    class Meta:
        model = Level
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    levels = serializers.SerializerMethodField(
        read_only=True)

    def get_levels(self, instance):
        public_levels = instance.levels.filter(is_public=True)
        return LevelSerializer(public_levels, many=True).data

    class Meta:
        model = HotlineUser
        fields = ['id', 'email', 'levels']
