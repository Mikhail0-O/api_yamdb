from django.shortcuts import get_object_or_404

from reviews.models import Reviews, Titles


class GetTitleMixin:
    def get_title(self):
        return get_object_or_404(Titles, id=self.kwargs['title_id'])


class GetReviewMixin:
    def get_review(self):
        return get_object_or_404(Reviews, id=self.kwargs['review_id'])
