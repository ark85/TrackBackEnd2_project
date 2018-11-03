# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.

# -*- coding: utf-8 -*-

class Like(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='likes',
        verbose_name='Author',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = 'id',
