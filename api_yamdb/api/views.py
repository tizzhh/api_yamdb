from random import randint

from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import (
    IsAdmin,
    IsAdminModerOrAuthorOrPostNew,
    IsAdminOrSuperUser,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CustomTokenObtainPairSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializerAdmin,
    UserSerializerAuth,
    UserSerializerReadPatch,
)
from custom_user.models import CustomUser
from reviews.models import Category, Genre, Review, Title


@api_view(['POST'])
def get_custom_token(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)
        refresh = RefreshToken.for_user(serializer.validated_data['USER'])
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetAuth(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerAuth

    def create(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(username=request.data.get('username'))
        serializer = self.get_serializer(data=request.data)
        if not user:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        if user and user[0].email != request.data.get('email'):
            raise BadRequest('Incorrect email')

        confirmation_code = randint(10000, 99999)
        self.send_confirmation_code_email(request.data, confirmation_code)

        user = CustomUser.objects.get(username=request.data.get('username'))
        user.confirmation_code = confirmation_code
        user.save()

        headers = self.get_success_headers(serializer.initial_data)

        return Response(
            serializer.initial_data, status=status.HTTP_200_OK, headers=headers
        )

    def send_confirmation_code_email(self, data, confirmation_code):
        send_mail(
            subject='Confirmation code',
            message=(
                f'Dear {data.get("username")}, here\'s your confirmation'
                'code: {confirmation_code}'
            ),
            from_email='yamdb@yamdb.net',
            recipient_list=(data.get('email'),),
            fail_silently=True,
        )


class UserViewSetAdmin(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerAdmin
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination


class UserViewSetReadPatch(viewsets.ModelViewSet):
    serializer_class = UserSerializerReadPatch
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(CustomUser, username=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModerOrAuthorOrPostNew,
    )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, title=self.get_title()
        )

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModerOrAuthorOrPostNew,
    )

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, review=self.get_review()
        )

    def get_queryset(self):
        return self.get_review().comments.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrSuperUser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminModerOrAuthorOrPostNew,)
    pagination_class = PageNumberPagination
    filter_backends = filters.SearchFilter
    search_fields = ('=category', '=genre', '=name', '=year')
    http_method_names = ['get', 'post', 'patch', 'delete']
