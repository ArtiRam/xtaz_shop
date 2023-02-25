# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def about_us(request):
    return render(request, 'about.html')


def blog(request):
    return render(request, 'blog.html')


def terms_conditions(request):
    return render(request, 'terms-conditions.html')



