from djoser.serializers import UserCreateSerializer
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer

from .models import Subscribers, User
from api.fields import Base64ImageField


class UserListSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'avatar')

    def get_is_subscribed(self, author):
        request = self.context.get('request')
        if request and not request.user.is_anonymous:
            return Subscribers.objects.filter(subscriber=request.user,
                                              subscribe_to=author).exists()
        return False


class UserCreatesSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class UserMeSerializer(UserListSerializer):
    pass


class AvatarSerializer(ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class SubscribeSerializer(UserListSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta(UserListSerializer.Meta):
        fields = UserListSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def validate(self, data):
        author = self.instance
        request = self.context['request']
        user = request.user
        if author == user:
            raise serializers.ValidationError('Нельзя подписаться на себя!',
                                              status.HTTP_400_BAD_REQUEST)
        if Subscribers.objects.filter(subscriber=user, subscribe_to=author
                                      ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!',
                status.HTTP_400_BAD_REQUEST)
        return data

    def get_recipes(self, author):
        from recipes.serializers import RecipForSubscribersSerializer
        recipes = author.recipes.all()
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipForSubscribersSerializer(recipes,
                                                   many=True,
                                                   read_only=True)
        return serializer.data

    def get_recipes_count(self, author):
        return author.recipes.count()
