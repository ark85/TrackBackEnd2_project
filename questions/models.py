# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings
from categories.models import Category
from likes.models import Like
from comments.models import Comment


class Question(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Question name'
    )
    content = models.CharField(
        max_length=500,
        verbose_name='Question content'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='questions',
        verbose_name='Author',
        on_delete=models.CASCADE
    )
    categories = models.ManyToManyField(
        Category,
        # Update faster than remove
        blank=True,
        related_name='questions',
        verbose_name='Question\'s categories'
    )
    likes = GenericRelation(Like)
    is_archive = models.BooleanField(
        default=False,
        verbose_name='Question in archive'
    )

    # Add answers and comments

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = 'name', 'id'
