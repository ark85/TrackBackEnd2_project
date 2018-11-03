# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "name",
    search_fields = "name",
