from wsgiref.util import request_uri
from django import  forms
from django.contrib.auth import authenticate, login, logout
from django.core.mail import forbid_multi_line_headers
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import title
from django.urls import reverse
from django.utils.text import normalize_newlines

from .models import User, booksmanage


# Create your views here.


def index(request):
    return render(request, "managesystem/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("select"))
        else:
            return render(request, "managesystem/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "managesystem/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "managesystem/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "managesystem/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "managesystem/register.html")

class NewTaskForm(forms.Form):
    book = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search Books'
        })
    )
def select(request):
    if request.method =="POST":
       form = NewTaskForm(request.POST)
       if form.is_valid():
           submit_name= form.cleaned_data["book"]
           if booksmanage.objects.filter(name=submit_name).exists():
              item = booksmanage.objects.get(name=submit_name)
              return render(request , "managesystem/page.html",{
                  "item":item
              })
           else:
               return HttpResponse("error")
       else:
           return HttpResponse("error")
    return render(request,"managesystem/select.html" , {
         "taskform":NewTaskForm()
    })

def borrowbook(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            submit_name = form.cleaned_data["book"]
            if booksmanage.objects.filter(name=submit_name).exists():
                item = booksmanage.objects.get(name=submit_name)
                item.is_active = False
                item.borrow = User.objects.get(username=request.user.username)
                item.save()
                return  HttpResponse("success")
            else:
                return HttpResponse("error")
        else:
            return HttpResponse("error")
    return render(request, "managesystem/borrow.html", {
        "borrowform": NewTaskForm()
    })

def back(request):
    user = User.objects.get(username=request.user.username)
    books = user.borrowed.all()
    if request.method =="POST":
       name = request.POST.get('borrowed')
       booker = booksmanage.objects.get(name=name)
       booker.is_active = True
       booker.borrow = None
       booker.save()
    return render(request , "managesystem/back.html",{
        "books":books
    })