# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from likes.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = "user",
    search_fields = "user__username",
