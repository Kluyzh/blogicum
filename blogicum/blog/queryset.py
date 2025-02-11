from django.db import models
from django.db.models import Count
from django.utils import timezone


class PostQuerySet(models.QuerySet):

    def filtered_posts(self, *select_related_args: str):
        return self.select_related(*select_related_args).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    def comments_count(self):
        return self.annotate(comment_count=Count('comments'))
