from django.urls import path

from api import views

urlpatterns = [
    path(
        'auth/signup/',
        views.UserViewSetAuth.as_view({'post': 'create'}),
        name='signup',
    ),
    path(
        'users/',
        views.UserViewSetAdmin.as_view(
            {
                'get': 'retrieve',
                'post': 'create',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='users-admin',
    ),
]
