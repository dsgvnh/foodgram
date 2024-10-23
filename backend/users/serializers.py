from rest_framework.serializers import ModelSerializer, ImageField
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from djoser.serializers import UserCreateSerializer
from django.core.files.base import ContentFile
from .models import User
import base64


class Base64ImageField(ImageField):
    """Сериализация изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'avatar')


class UserCreatesSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class UserMeSerializer(UserListSerializer):
    def to_representation(self, instance):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            raise AuthenticationFailed('Учетные данные не были предоставлены.',
                                       code=401)
        return super().to_representation(instance)


class AvatarSerializer(ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)
