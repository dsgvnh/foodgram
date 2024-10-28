from django.urls import path, include
from .views import AvatarPutDeleteView, SubcribeView

app_name = 'users'


urlpatterns = [
    path('', include('djoser.urls')),
    path('users/me/avatar/', AvatarPutDeleteView.as_view()),
    path('users/<int:pk>/subscribe/', SubcribeView.as_view()),
    path('auth/', include('djoser.urls.authtoken'))
]
