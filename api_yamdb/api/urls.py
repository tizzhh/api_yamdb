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
api_v1_router.register('users', views.UserViewSetAdmin, basename='users')

urlpatterns = [
    path(
        'v1/auth/signup/',
        views.user_view_set_auth,
        name='signup',
    ),
    path('v1/auth/token/', views.get_yamdb_user_token, name='jwt-token'),
    path('v1/', include(api_v1_router.urls)),
]
