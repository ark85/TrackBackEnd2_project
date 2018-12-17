# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils.decorators import method_decorator
from jsonrpc import jsonrpc_method

from categories.models import Category
from core.models import User
from likes.services import add_like
from questions.models import Question
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from questions.forms import QuestionViewsForm


class QuestionDetails(DetailView):
    model = Question
    fields = 'content'
    context_object_name = 'question'
    template_name = 'questions/question_details.html'

    def get_object(self):
        question_id = self.kwargs.get("question_id")
        return get_object_or_404(Question, id=question_id)

    def get_queryset(self):
        queryset = super(QuestionDetails, self).get_queryset()
        queryset = queryset.filter(is_archive=False)
        return queryset

    def get_success_url(self):
        return reverse('questions:question_details', kwargs={'question_id': self.object.pk})


class QuestionViews(ListView):
    questions = Question

    def get_queryset(self):
        queryset = Question.objects.all()
        queryset = queryset.filter(is_archive=False)
        return queryset

    def get(self, request, *args, **kwargs):
        questions = self.get_queryset()
        form = QuestionViewsForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data['sort']:
                questions = questions.order_by(data['sort'])
            if data['search']:
                questions = questions.filter(name__icontains=data['search'])
        context = {
            'questions': questions,
            'questions_form': form
        }

        return render(request, "questions/question_views.html", context)


@method_decorator(login_required, name='dispatch')
class QuestionEdit(UpdateView):
    model = Question
    fields = 'name', 'categories'
    context_object_name = 'question'
    template_name = 'questions/question_edit.html'

    def get_queryset(self):
        queryset = super(QuestionEdit, self).get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('questions:question_details', kwargs={'question_id': self.object.pk})


@method_decorator(login_required, name='dispatch')
class QuestionCreate(CreateView):

    model = Question
    fields = 'name', 'categories'
    context_object_name = 'question'
    template_name = 'questions/question_create.html'

    def get(self, request):
        form = self.get_form()
        return render(request, 'questions/question_create.html', {'form': form})

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('questions:question_details', question_id=question.pk)
        else:
            return render(request, 'questions/question_create.html', {'form': form})

    def get_success_url(self):
        return reverse('questions:question_details', kwargs={'question_id': self.object.pk})


def question_like(request):
    add_like(Question.objects.get(0), request.POST.user)


@jsonrpc_method('question.details')
def question_details(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = {
        'result': 'success',
        'question': json.loads(serializers.serialize("json", [question, ])),
        'answer': json.loads(serializers.serialize("json", question.answers.all().filter(is_archive=False))),
    }
    return context


@jsonrpc_method('question.views')
def question_views(request):
    questions = Question.objects.all()
    form = QuestionViewsForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        if data['sort']:
            questions = questions.order_by(data['sort'])
        if data['search']:
            questions = questions.filter(name__icontains=data['search'])
    context_json = {
        'result': 'success',
        'questions': json.loads(serializers.serialize("json", questions))
    }
    return context_json


@jsonrpc_method('question.create', authenticated=True)
def question_create(request, name, content, author, categories=None, is_archive=None):
    if request.method == 'POST':
        if is_archive is None:
            archive = False
        else:
            archive = is_archive
        category_list = []
        if categories is not None:
            categories = Category.objects.all()
            for category in categories:
                category_list.append(categories.filter(name=category))
        user = User.objects.get(username=author)
        question = Question(name=name, content=content, author=user, is_archive=archive, categories=category_list)
        question.save()
        return {"result": "success"}
    return {"error": "not post"}


@jsonrpc_method('category.edit')
def category_edit(request, question_id, author, name=None, content=None, categories=None, is_archive=None):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        if name is not None:
            question.name = name
        if content is not None:
            question.content = content
        if categories is not None:
            category_list = []
            categories = Category.objects.all()
            for category in categories:
                category_list.append(categories.filter(name=category))
            question.categories = category_list
        if is_archive is not None:
            question.is_archive = is_archive
        user = User.objects.get(username=author)
        question.author = user
        question.save()
        return {"result": "success"}
    return {"error": "not post"}
