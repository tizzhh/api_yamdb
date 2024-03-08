from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Review, Title


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
        if request.method == 'POST' and Review.objects.filter(
                author=request.user, title=title
        ).exists():
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
