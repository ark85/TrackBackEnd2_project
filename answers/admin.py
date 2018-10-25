# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from answers.models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = "content", "author"
    search_fields = "question", "author__username"
    list_filter = 'is_archive',