from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersMeViewSet

app_name = 'users'

router_v1 = DefaultRouter()

#router_v1.register('users', UsersViewSet)

urlpatterns = [
    #path('', include(router_v1.urls)),
    #path('users/me/', UsersMeViewSet),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
