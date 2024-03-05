from django.urls import path

from api import views

urlpatterns = [
    path('auth/signup/', views.UserViewSet.as_view({'post': 'create'})),
]
