# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        verbose_name='Author'
    )
    likes = models.ManyToManyField(
        Like,
        blank=True,
        related_name="answer_likes"
    )
    comments = models.ManyToManyField(
        Comment,
        blank=True,
        related_name="answer_comments"
    )
    question = models.ForeignKey(
        Question,
        related_name='answers',
        verbose_name='Answer\'s question'
    )
    is_archive = models.BooleanField(
        default=False,
        verbose_name='Answer in archive'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = 'content', 'id'