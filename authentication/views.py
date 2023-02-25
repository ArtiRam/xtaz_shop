# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.views.generic import TemplateView
from .forms import RegisterForm, LoginForm


class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get(self, request, **kwargs):
        user_form = RegisterForm()
        context = {'user_form': user_form}
        return render(request, 'auth/register.html', context)

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')
        context = {'user_form': user_form}
        return render(request, 'auth/register.html', context)


class LoginView(TemplateView):
    template_name = 'auth/login.html'

    def get(self, request, **kwargs):
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'auth/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('index')

        context = {'login_form': login_form}
        return render(request, 'auth/login.html', context)


def logout_user(request):
    logout(request)
    return redirect("index")
