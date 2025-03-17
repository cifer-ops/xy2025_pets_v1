import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from .models import UserProfile
from .forms import LoginForm
import os
import time
from django.conf import settings
@login_required
def my_info(request):
    try:
        user = request.user
        if request.method == "GET":
            return render(request, "my_info.html", locals())
        if request.method == "POST":
            username = request.POST.get("username", "")
            mobile = request.POST.get("mobile", "")
            email = request.POST.get("email", "")
            print(username)
            print(mobile)
            print(email)
            if username == "" or username == None or len(username) < 6:
                msg = "The username cannot be empty, it must be greater than 6 digits."
                return render(request, "my_info.html", locals())
            if mobile == "" or mobile == None or len(mobile) != 11:
                msg = "The mobile phone number cannot be empty, it must be 11 bits and the format is correct"
                return render(request, "my_info.html", locals())

            user.username = username
            user.mobile = mobile
            user.email = email
            user.save()
            msg = "Modification was successful"
            return render(request, "my_info.html", locals())
    except Exception as e:
        print(e)
        msg = "System Error"
        return render(request, "my_info.html", locals())

def do_register(request):
    try:
        msg = ""
        if request.method == "GET":
            return render(request, "register.html", locals())
        if request.method == "POST":
            user = request.user
            datas = request.POST
            username = request.POST.get("username")
            mobile = request.POST.get("mobile")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            if len(mobile) == 0 or len(mobile) != 11:
                msg = "Mobile phone number format error"
                return render(request, "register.html", locals())
            if len(username) < 6 or len(password) < 6 or len(password2) < 6:
                msg="The account password must be greater than 6 digits"
                return render(request, "register.html", locals())
            if password != password2:
                msg="The passwords entered twice are inconsistent"
                return render(request, "register.html", locals())
            only = UserProfile.objects.filter(username=username)
            if len(only) > 0:
                msg = "The username already exists"
                return render(request, "register.html", locals())

            new_user = UserProfile()
            new_user.username = username
            new_user.mpassword = password
            new_user.mobile = mobile
            new_user.email = email
            new_user.set_password(password)
            new_user.save()
            return redirect("accounts:login")
        else:
            return render(request, "register.html", locals())
    except Exception as e:
        print(e)
        msg = "System error failed to add"
        return render(request, "register.html", locals())


def user_login(request):
    try:
        if request.user.is_authenticated:
            return redirect("/")
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    # user.backend = 'django.contrib.auth.backends.ModelBackend' # Specify the default login verification method
                    login(request, user)
                    if user.is_superuser:
                        return redirect("/admin")
                    else:
                        return redirect("/")
                else:
                    errorinfo = "Incorrect account or password"
                    return render(request, 'login.html', {'login_form': login_form, "errorinfo":errorinfo})

            else:
                errorinfo = "Incorrect account or password or incorrect format"
                return render(request, 'login.html', {'login_form': login_form, "errorinfo":errorinfo})
        else:
            login_form = LoginForm()
            return render(request, 'login.html', {'login_form': login_form})
    except Exception as e:
        login_form = LoginForm()
        print(e)
        errorinfo = "System Error"
        return render(request, 'login.html', {'login_form': login_form, "errorinfo":errorinfo})


@login_required
def user_logout(request):
    try:
        logout(request)
        return redirect('accounts:login')
    except Exception as e:
        print(e)
    return render(request, "error.html", {"msg":"Exit error"})

