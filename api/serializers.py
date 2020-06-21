from rest_framework import serializers

from .models import HotlineUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotlineUser
        fields = ['id', 'email',]