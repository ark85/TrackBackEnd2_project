# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from likes.models import Like

# Create your models here.

# -*- coding: utf-8 -*-

class Comment(models.Model):

    content = models.CharField(
        max_length=500,
        verbose_name='Comment content'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        verbose_name='Author',
        on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(
        Like,
        blank=True,
        related_name="comment_likes",
        verbose_name='Comment\'s likes'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = 'id',