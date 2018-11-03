# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View
from core.forms import RegisterForm
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, "core/index.html", {})


class Register(View):
    form_class = RegisterForm
    template_name = 'core/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("categories:categories")

        return render(request, self.template_name, {'form': form})


class Login(LoginView):
    template_name = 'core/login.html'

    def get_success_url(self):
        return reverse('categories:categories')


class Logout(LogoutView):
    template_name = 'core/logout.html'

    def get_success_url(self):
        return reverse('core:login')
