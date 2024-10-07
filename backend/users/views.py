from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from .pagination import UsersPagination
from .serializers import UserListSerializer, UserCreateSerializer
from rest_framework.permissions import SAFE_METHODS
from djoser.views import UserViewSet
from djoser.permissions import CurrentUserOrAdmin
User = get_user_model()


class UsersMeViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticated, )

    @action(methods=['GET',], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserListSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
