from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from reviews.models import Review, Title
from .permission import IsAdminModerOrAuthor
from .serializers import CommentSerializer, ReviewSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAdminModerOrAuthor
    )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuethenticatedOrReadOnly, IsAdminModerOrAuthor
    )

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_review()
        )

    def get_queryset(self):
        return self.get_review().comments.all()
