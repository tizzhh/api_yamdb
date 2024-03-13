from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title, YamdbUser
from yamdb_user.models import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
    BaseUserValidator,
)


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['username'] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']
        user = get_object_or_404(YamdbUser, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Incorrect confirmation code')
        attrs['USER'] = user
        return attrs


class UserSerializerAuth(serializers.Serializer, BaseUserValidator):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
    )
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        errors = {}
        email_exists = YamdbUser.objects.filter(email=email).exists()
        username_exists = YamdbUser.objects.filter(username=username).exists()
        if (
            not email_exists and not username_exists
        ) or YamdbUser.objects.filter(email=email, username=username).exists():
            return attrs
        if email_exists:
            errors['email'] = 'Email already exists'
        if username_exists:
            errors['username'] = 'Username already exists'
        raise serializers.ValidationError(errors)

    def create(self, validated_data):
        user = YamdbUser.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user[0])
        self.send_confirmation_code_email(validated_data, confirmation_code)

        return user

    def send_confirmation_code_email(self, data, confirmation_code):
        send_mail(
            subject='Confirmation code',
            message=(
                f'Dear {data.get("username")}, here\'s your confirmation'
                f'code: {confirmation_code}'
            ),
            from_email=settings.YAMBD_EMAIL,
            recipient_list=(data.get('email'),),
            fail_silently=True,
        )


class UserSerializerAdmin(serializers.ModelSerializer, BaseUserValidator):
    class Meta:
        model = YamdbUser
        fields = (
            'username',
            'email',
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
        if request.method != 'POST':
            return data
        if Review.objects.filter(
            author=request.user,
            title__id=self.context['view'].kwargs['title_id'],
        ).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв к произведению.'
            )
        return data


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


class TitleReadSerializer(serializers.ModelSerializer):
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
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_null=False,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
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
            'category'
        )

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data
