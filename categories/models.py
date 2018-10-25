# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Category(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name='Category name'
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    # Create author for old categories --- Done

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = 'name', 'id'