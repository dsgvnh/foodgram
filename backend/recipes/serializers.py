from rest_framework import serializers
from .models import Tag, Ingredient, Recipes
from django.core.files.base import ContentFile
from users.serializers import UserListSerializer
import base64


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_amount(self, value):
        if value <= 0:
            return serializers.ValidationError('Минимальное значение - 1')
        return value


class RecipSerializer(serializers.ModelSerializer):
    author = UserListSerializer(required=False)
    tags = TagSerializer(many=True, read_only=True)
    image = serializers.CharField(max_length=None, allow_blank=True)
    ingredients = IngredientSerializer(many=True, read_only=True,)
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Recipes
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def create_avatar(self, avatar_base64):
        format, imgstr = avatar_base64.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=f"avatar.{ext}")

    def update(self, instance, validated_data):
        if 'avatar' in validated_data:
            avatar_base64 = validated_data.pop('avatar')
            instance.avatar = self.create_avatar(avatar_base64)
        return super().update(instance, validated_data)

    def validate_tags(self, data):
        if data is None:
            raise serializers.ValidationError('Должен быть хотя бы 1 тег')
        return data

    def validate_ingredients(self, data):
        if data is None:
            raise serializers.ValidationError(
                'Должен быть хотя бы 1 ингредиент')
        return data
