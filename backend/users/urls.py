from django.urls import path, include
from .views import AvatarPutDeleteView

app_name = 'users'

urlpatterns = [
    path('', include('djoser.urls')),
    path('users/me/avatar/', AvatarPutDeleteView.as_view()),
    path('auth/', include('djoser.urls.authtoken'))
]
