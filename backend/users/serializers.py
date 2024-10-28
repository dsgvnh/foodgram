from rest_framework.serializers import ModelSerializer, ImageField
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from djoser.serializers import UserCreateSerializer
from django.core.files.base import ContentFile
from .models import User, Subscribers
from recipes.models import Recipes
import base64


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserListSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'avatar')
    
    def get_is_subscribed(self, author):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Subscribers.objects.filter(subscriber=user, subscribe_to=author).exists()


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


class SubscribeSerializer(UserListSerializer):
    recipes = serializers.SerializerMethodField(default=0)
    recipes_count = serializers.SerializerMethodField(default=5)

    class Meta(UserListSerializer.Meta):
        fields = UserListSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def validate(self, data):
        author = self.instance
        request = self.context['request']
        user = request.user
        if author == user:
            raise serializers.ValidationError('Нельзя подписаться на себя!', 400)
        if Subscribers.objects.filter(subscriber=user, subscribe_to=author).exists():
            raise serializers.ValidationError('Вы уже подписаны на этого пользователя!', 400)
        return data

    def get_recipes(self, author):
        from recipes.serializers import RecipForSubscribersSerializer
        recipes = author.recipes.all()
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        if limit and recipes:
            recipes = recipes[:int(limit)]
            serializer = RecipForSubscribersSerializer(recipes, many=True, read_only=True)
            return serializer.data
        else:
            return recipes
    
    def get_recipes_count(self, author):
        return author.recipes.count()