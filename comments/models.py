# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings


class Comment(models.Model):
    content = models.CharField(
        max_length=500,
        verbose_name='Comment content'
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='comments',
                               on_delete=models.CASCADE)
    is_archive = models.BooleanField(
        default=False,
        verbose_name='Answer in archive'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = 'id',
