from django.urls import include, path

from .views import AvatarPutDeleteView, SubcribeView, SubscribeListView

app_name = 'users'


urlpatterns = [
    path('users/subscriptions/', SubscribeListView.as_view()),
    path('', include('djoser.urls')),
    path('users/me/avatar/', AvatarPutDeleteView.as_view()),
    path('users/<int:pk>/subscribe/', SubcribeView.as_view()),
    path('auth/', include('djoser.urls.authtoken'))
]
