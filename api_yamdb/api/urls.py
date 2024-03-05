from django.urls import path

from api import views

urlpatterns = [
    path(
        'auth/signup/',
        views.UserViewSetAuth.as_view({'post': 'create'}),
        name='signup',
    ),
    path('auth/token/', views.get_custom_token, name='jwt-token'),
    path(
        'users/',
        views.UserViewSetAdmin.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name='users-admin',
    ),
    path(
        'users/me/',
        views.UserViewSetReadPatch.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
            }
        ),
        name='users-me',
    ),
    path(
        'users/<slug:username>/',
        views.UserViewSetAdmin.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='users-admin',
    ),
]
