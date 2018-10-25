# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        verbose_name='Author'
    )
    categories = models.ManyToManyField(
        Category,
        # Update faster than remove
        blank=True,
        related_name='questions',
        verbose_name='Question\'s categories'
    )
    likes = models.ManyToManyField(
        Like,
        blank=True,
        related_name="question_likes",
        verbose_name='Question\'s likes'
    )
    comments = models.ManyToManyField(
        Comment,
        blank=True,
        related_name="question_comments",
        verbose_name='Question\'s comments'
    )
    is_archive = models.BooleanField(
        default=False,
        verbose_name='Question in archive'
    )

    # Add answers and comments

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = 'name', 'id'