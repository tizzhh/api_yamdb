from random import randint

from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .filters import TitleFilter

from .permissions import IsAdminModerOrAuthorOrPostNew, IsAdminOrSuperUser
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CustomTokenObtainPairSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
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
                f'code: {confirmation_code}'
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
    http_method_names = ('get', 'post', 'patch', 'delete')

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
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, review=self.get_review()
        )

    def get_queryset(self):
        return self.get_review().comments.all()


class CategoryGenreBaseViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (
        IsAdminOrSuperUser | DjangoModelPermissionsOrAnonReadOnly,
    )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'name'
    )
    serializer_class = TitleReadSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAdminOrSuperUser | DjangoModelPermissionsOrAnonReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateSerializer
        return TitleReadSerializer
