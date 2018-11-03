# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils.decorators import method_decorator

from answers.models import Answer
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DetailView


class AnswerDetails(DetailView):
    model = Answer
    fields = 'content'
    context_object_name = 'answer'
    template_name = 'answers/answer_details.html'

    def get_object(self):
        answer_id = self.kwargs.get("answer_id")
        return get_object_or_404(Answer, id=answer_id)

    def get_queryset(self):
        queryset = super(AnswerDetails, self).get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('answers:answer_details', kwargs={'answer_id': self.object.pk})


@method_decorator(login_required, name='dispatch')
class AnswerEdit(UpdateView):
    model = Answer
    fields = 'content'
    context_object_name = 'answer'
    template_name = 'answers/answer_edit.html'

    def get_queryset(self):
        queryset = super(AnswerEdit, self).get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('answers:answer_details', kwargs={'answer_id': self.object.pk})


@method_decorator(login_required, name='dispatch')
class AnswerCreate(CreateView):

    model = Answer
    fields = 'content', 'question'
    context_object_name = 'answer'
    template_name = 'answers/answer_create.html'

    def get(self, request):
        form = self.get_form()
        return render(request, 'answers/answer_create.html', {'form': form})

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.save()
            # return redirect('answers:answer_details', answer_id=answer.pk)
            return redirect('questions:questions')
        else:
            return render(request, 'answers/answer_create.html', {'form': form})

    def get_success_url(self):
        return reverse('answers:answer_details', kwargs={'answer_id': self.object.pk})
