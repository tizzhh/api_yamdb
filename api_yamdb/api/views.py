from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound
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

from .permissions import (
    IsAdminModerOrAuthor,
    IsAdminOrSuperUser,
    IsAdminOrSuperUserReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CustomTokenObtainPairSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    UserSerializerAdmin,
    UserSerializerAuth,
    UserSerializerReadPatch,
)
from reviews.models import Category, Genre, Review, Title, YamdbUser


@api_view(['POST'])
def get_custom_token(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    refresh = serializer.get_token(serializer.validated_data['USER'])
    return Response(
        {
            'token': str(refresh.access_token),
        },
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
def user_view_set_auth(request):
    serializer = UserSerializerAuth(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.initial_data,
        status=status.HTTP_200_OK,
    )


class UserViewSetAdmin(viewsets.ModelViewSet):
    queryset = YamdbUser.objects.all()
    serializer_class = UserSerializerAdmin
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me',
    )
    def retrieve_me(self, request):
        serializer = UserSerializerReadPatch(
            self.request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data)


class UserViewSetReadPatch(viewsets.ModelViewSet):
    serializer_class = UserSerializerReadPatch
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(YamdbUser, username=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModerOrAuthor,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

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
        IsAdminModerOrAuthor,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user, review=self.get_review()
        )

    def get_queryset(self):
        return self.get_review().comments.all()


class GenreViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrSuperUserReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoryViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrSuperUserReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'id'
    )
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrSuperUserReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        elif self.action in ['create', 'patch']:
            return TitleCreateSerializer
        return TitleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        year = self.request.query_params.get('year')
        name = self.request.query_params.get('name')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if year:
            queryset = queryset.filter(year=year)
        if name:
            queryset = queryset.filter(name=name)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        if 'category' in request.data:
            category_slug = request.data['category']
            try:
                category_instance = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                raise NotFound(
                    f"Category with slug '{category_slug}' does not exist"
                )
            instance.category = category_instance

        self.perform_update(serializer)
        return Response(serializer.data)
