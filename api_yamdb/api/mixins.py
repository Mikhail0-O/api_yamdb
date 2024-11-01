from django.shortcuts import get_object_or_404
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import filters

from reviews.models import Review, Title
from .permissions import IsAdminOrReadOnly, IsAdminAuthorModeratorOrReadOnly


class GetTitleMixin:
    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])


class GetReviewMixin:
    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])


class UpdateMethodMixin:
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


class IsAdminOrReadOnlyMixin:
    permission_classes = [IsAdminOrReadOnly]


class IsAdminAuthorModeratorOrReadOnlyMixin:
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]


class SearchFilterMixin:
    filter_backends = (filters.SearchFilter,)
