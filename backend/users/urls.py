from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import pass_view

app_name = 'users'

router_v1 = DefaultRouter()

#router_v1.register('users', pass_view())

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
