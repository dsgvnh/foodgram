from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import DefaultPagination

from .models import Subscribers
from .serializers import AvatarSerializer, SubscribeSerializer

User = get_user_model()


class UserMeViewSet(UserViewSet):
    permission_classes = [IsAuthenticated]

    def me(self, request):
        return Response(self.get_serializer(request.user).data)


class AvatarPutDeleteView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = AvatarSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = get_object_or_404(User, username=request.user)
        if user.avatar:
            user.avatar.delete(save=False)
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Аватар отсутствует',
                        status=status.HTTP_400_BAD_REQUEST)


class SubcribeView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        user = request.user
        subscribe_to = get_object_or_404(User, id=pk)
        serializer = SubscribeSerializer(subscribe_to, data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        Subscribers.objects.create(subscriber=user, subscribe_to=subscribe_to)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        unsub_author = get_object_or_404(User, id=pk)
        if Subscribers.objects.filter(subscriber=user,
                                      subscribe_to=unsub_author).exists():
            Subscribers.objects.filter(subscriber=user,
                                       subscribe_to=unsub_author).delete()
            return Response({'Сообщение': 'Вы успешно отписались от автора!'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Ошибка': 'Вы не были подписаны на автора!'},
                            status=status.HTTP_400_BAD_REQUEST)


class SubscribeListView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = DefaultPagination

    def get(self, request):
        paginator = self.pagination_class()
        user = request.user
        subscriptions = Subscribers.objects.filter(subscriber=user)
        pag_subs = paginator.paginate_queryset(subscriptions, request)
        subscribed_users = [subscription.subscribe_to
                            for subscription in pag_subs]
        serializer = SubscribeSerializer(subscribed_users, many=True,
                                         context={'request': request})
        return paginator.get_paginated_response(serializer.data)
