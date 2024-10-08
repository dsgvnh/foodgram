from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import AvatarSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.decorators import login_required


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