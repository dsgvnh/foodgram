from django.urls import include, path

from rest_framework.routers import DefaultRouter

from recipes.views import IngredientsViewSet, RecipViewSet, TagsViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagsViewSet)
router_v1.register('ingredients', IngredientsViewSet)
router_v1.register(r'recipes', RecipViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('users.urls'))
]
