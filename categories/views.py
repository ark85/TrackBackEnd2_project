# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse

from categories.forms import CategoryViewsForm
from categories.models import Category
from core.models import User
from django.views.generic import UpdateView, ListView
from django.views.generic import CreateView
from django.views.generic import DetailView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from jsonrpc import jsonrpc_method


class CategoryDetails(DetailView):
    categories = Category.objects.all()

    def get_object(self, queryset=categories):
        category_id = self.kwargs.get("category_id")
        return get_object_or_404(Category, id=category_id)

    def get_context_data(self):
        context = {
            'category': self.get_object(),
            'questions': self.get_object().questions.all().filter(is_archive=False)
        }
        return context

    def get(self, request, *args, **kwargs):
        return render(request, "categories/category_details.html", self.get_context_data())


class CategoryViews(ListView):
    categories = Category

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        categories = self.get_queryset()
        form = CategoryViewsForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data['sort']:
                categories = categories.order_by(data['sort'])
            if data['search']:
                categories = categories.filter(name__icontains=data['search'])
        context = {
            'categories': categories,
            'form': form
        }

        return render(request, "categories/category_views.html", context)


@method_decorator(login_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Category
    fields = 'name'

    def get(self, request, **kwargs):
        form = self.get_form()
        return render(request, 'categories/category_create.html', {'form': form})

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            return redirect('categories:categories')
        else:
            return render(request, 'categories/category_create.html', {'form': form})

    def get_success_url(self):
        return reverse('categories:category_details', kwargs={'category_id': self.object.pk})


@method_decorator(login_required, name='dispatch')
class CategoryEdit(UpdateView):
    model = Category
    fields = 'name',
    context_object_name = 'category'
    template_name = 'categories/category_edit.html'

    def get_queryset(self):
        queryset = super(CategoryEdit, self).get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('categories:category_details', kwargs={'category_id': self.object.pk})

    def form_valid(self, form):
        response = super(CategoryEdit, self).form_valid(form)
        return HttpResponse('valid')


@jsonrpc_method('category.details')
def category_details(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {
        'result': 'success',
        'category': serializers.serialize("json", [category, ]),
        'questions': serializers.serialize("json", category.questions.all().filter(is_archive=False))
    }
    return context


@jsonrpc_method('category.views')
def category_views(request):
    categories = Category.objects.all()
    form = CategoryViewsForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        if data['sort']:
            categories = categories.order_by(data['sort'])
        if data['search']:
            categories = categories.filter(name__icontains=data['search'])
    context_json = {
        'result': 'success',
        'categories': serializers.serialize("json", categories)
    }
    return context_json


# @jsonrpc_method('category.create')
# def category_create(request, name, author):
#     user = User.objects.get(username=author)
#     category = Category(name=name, author=user)
#     category.save()
#     return {"result": "success"}


@jsonrpc_method('category.edit')
def category_edit(request):
    pass