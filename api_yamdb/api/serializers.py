from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from reviews.models import Category, Comment, Genre, Review, Title, YamdbUser


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['username'] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = get_object_or_404(YamdbUser, username=username)
        if confirmation_code != user.confirmation_code:
            raise forms.ValidationError('Incorrect confirmation code')
        attrs['USER'] = user
        return attrs


# class BaseUserSerializer(serializers.ModelSerializer):
class BaseUserSerializer:
    # class Meta:
    #     model = YamdbUser
    #     fields = (
    #         'username',
    #         'email',
    #     )

    def validate_username(self, value):
        if value == 'me':
            raise forms.ValidationError('Username cannot be "me"')
        return value


class UserSerializerAuth(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    # email = serializers.EmailField(max_length=254)

    class Meta:
        model = YamdbUser
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise forms.ValidationError('Username cannot be "me"')
        return value

    # def create(self, validated_data):
    #     return YamdbUser.objects.create(**validated_data)
    # def validate_username(self, value):
    #     if value == 'me':
    #         raise forms.ValidationError('Username cannot be "me"')
    #     return value


class UserSerializerAdmin(UserSerializerAuth):
    class Meta(UserSerializerAuth.Meta):
        # model = YamdbUser
        fields = UserSerializerAuth.Meta.fields + (
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserSerializerReadPatch(UserSerializerAdmin):
    class Meta(UserSerializerAdmin.Meta):
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Checks user can create only one review for one title."""
        request = self.context['request']
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(
                author=request.user, title=title
            ).exists()
        ):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв к произведению.'
            )
        return data

    def validate_score(self, value):
        """Checks validity of rating value."""
        if 1 > value > 10:
            raise serializers.ValidationError(
                'Допустимые значения оценки: от 1 до 10.'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
