from rest_framework.serializers import ModelSerializer
from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.core.files.base import ContentFile
from .models import User
import base64


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
    avatar = serializers.CharField(max_length=None, allow_blank=True)

    class Meta:
        model = User
        fields = ('avatar',)

    def create_avatar(self, avatar_base64):
        format, imgstr = avatar_base64.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=f"avatar.{ext}")

    def update(self, instance, validated_data):
        if 'avatar' in validated_data:
            avatar_base64 = validated_data.pop('avatar')
            instance.avatar = self.create_avatar(avatar_base64)
        return super().update(instance, validated_data)
