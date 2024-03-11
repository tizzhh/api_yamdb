from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

api_v1_router = DefaultRouter()
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)
api_v1_router.register('genres', views.GenreViewSet, basename='genres')
api_v1_router.register(
    'categories', views.CategoryViewSet, basename='categories'
)
api_v1_router.register('titles', views.TitleViewSet, basename='titles')


urlpatterns = [
    path(
        'v1/auth/signup/',
        views.UserViewSetAuth.as_view({'post': 'create'}),
        name='signup',
    ),
    path('v1/auth/token/', views.get_custom_token, name='jwt-token'),
    path(
        'v1/users/',
        views.UserViewSetAdmin.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name='users-admin',
    ),
    path(
        'v1/users/me/',
        views.UserViewSetReadPatch.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
            }
        ),
        name='users-me',
    ),
    path(
        'v1/users/<slug:username>/',
        views.UserViewSetAdmin.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='users-admin',
    ),
    path('v1/', include(api_v1_router.urls)),
]
