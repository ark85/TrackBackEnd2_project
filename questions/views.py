# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils.decorators import method_decorator
from jsonrpc import jsonrpc_method

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
        'question': serializers.serialize("json", [question, ]),
        'answer': serializers.serialize("json", question.answers.all().filter(is_archive=False)),
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
        'questions': serializers.serialize("json", questions)
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