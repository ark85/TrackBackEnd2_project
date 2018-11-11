# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings

from questions.models import Question
from likes.models import Like
from comments.models import Comment


# Create your models here.

# -*- coding: utf-8 -*-

class Answer(models.Model):
    content = models.CharField(
        max_length=500,
        verbose_name='Answer content'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='answers',
        verbose_name='Author',
        on_delete=models.CASCADE
    )
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    question = models.ForeignKey(
        Question,
        related_name='answers',
        verbose_name='Answer\'s question',
        on_delete=models.CASCADE
    )
    is_archive = models.BooleanField(
        default=False,
        verbose_name='Answer in archive'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def get_comments(self):
        return self.comments

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = 'content', 'id'
