# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-
from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = "content", "user"
    search_fields = "content", "user__username"
    list_filter = 'is_archive',