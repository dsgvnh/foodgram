from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import AvatarSerializer, SubscribeSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Subscribers
from api.pagination import SubsPagination

User = get_user_model()


class AvatarPutDeleteView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        user = User.objects.get(username=request.user)
        serializer = AvatarSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = User.objects.get(username=request.user)
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
        serializer = SubscribeSerializer(subscribe_to, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        Subscribers.objects.create(subscriber=user, subscribe_to=subscribe_to)
        return Response(serializer.data, status=201)


class SubscribeListView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = SubsPagination

    def get(self, request):
        paginator = self.pagination_class()
        user = request.user
        subscriptions = Subscribers.objects.filter(subscriber=user)
        pag_subs = paginator.paginate_queryset(subscriptions, request)
        subscribed_users = [subscription.subscribe_to for subscription in pag_subs]
        serializer = SubscribeSerializer(subscribed_users, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
