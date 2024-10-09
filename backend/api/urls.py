from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import TagsViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('users.urls'))
]
