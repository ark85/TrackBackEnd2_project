# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from likes.models import Like


class Comment(models.Model):
    content = models.CharField(
        max_length=500,
        verbose_name='Comment content'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments',
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    likes = GenericRelation(Like)

    is_archive = models.BooleanField(
        default=False,
        verbose_name='Answer in archive'
    )

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = 'id',
