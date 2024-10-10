from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import TagsViewSet, IngredientsViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagsViewSet)
router_v1.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('users.urls'))
]
