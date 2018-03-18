# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html', {})

def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    # a HTTP request?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # save the new category to the database
            form.save(commit=True)
            return HttpResponseRedirect(reverse('rango:index', args=()))
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    cat = get_object_or_404(Category,slug=category_name_slug)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return HttpResponseRedirect(reverse('rango:category', args=(category_name_slug,)))
            else:
                print form.errors
    else:
        form = PageForm()
    context_dict = {'form':form, 'category':cat}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            # save the users form data to the database
            user = user_form.save()
            # hash password with set_password method
            user.set_password(user.password)
            # save again
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm({'name':' ', 'email':' ', 'password':' '})
    return render(request, 'rango/register.html', {'user_form':user_form, 'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index', args=()))
            else:
                return HttpResponse("Your rango account is disabled")
        else:
            return HttpResponse("Invalid login")
    else:
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index', args=()))
