from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json

import os
import time
from django.conf import settings
from .models import PetsType, PetsInfo, Collect, Adoption
# Create your views here.

def getPage(request, article_list):
    paginator = Paginator(article_list, 12)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


@login_required
def index(request):
    try:
        recommends = PetsInfo.objects.order_by('?')[:4]
        print(recommends)
    except Exception as e:
        print(e)
    return render(request, "index.html", locals())


@login_required
def pets(request):
    try:
        all_types = PetsType.objects.filter()
        area_alist = []
        age_alist = []
        areas = PetsInfo.objects.values('area').annotate(myArea=Count('area'))
        print(areas)
        for area in areas:
            if area["area"] not in area_alist:
                area_alist.append(area["area"])
        ages = PetsInfo.objects.values('age').annotate(myAge=Count('age'))
        print(ages)

        for age in ages:
            if age["age"] not in age_alist:
                age_alist.append(age["age"])

        user = request.user
        category = request.GET.get("category", "")
        key = request.GET.get("key", "")
        age = request.GET.get("age", "")
        area = request.GET.get("area", "")
        pets = PetsInfo.objects.filter()
        if category != "":
            category_obj = PetsType.objects.filter(id=category)
            if len(category_obj) > 0:
                category_obj = category_obj[0]
                pets = pets.filter(atype=category_obj)
            else:
                reason = "Sorry, the category does not exist or has been deleted!!!"
                return render(request, "error.html", locals())

        if key != "":
            pets = pets.filter(name__icontains=key)

        if age != "":
            pets = pets.filter(age=age)
        if area != "":
            pets = pets.filter(area=area)

        article_list = pets.filter().order_by("-updated")
        print("----------------")
        print(article_list)
        article_list = getPage(request, article_list)
        print(article_list)
    except Exception as e:
        print(e)
    return render(request, "pets.html", locals())



@login_required
def my_colloect(request):
    user = request.user
    all_types = PetsType.objects.filter()
    try:
        if request.method == "GET":
            colls = Collect.objects.filter(user=user)
            return render(request, "my_collect.html", locals())
    except Exception as e:
        print(e)
        reason = "Error: System error"
        return render(request, "error.html", locals())

@csrf_exempt
def add_collect(request):
    try:
        user = request.user
        datas = json.loads(request.body)
        print(datas)
        id = datas["id"]
        print(id)
        wb = PetsInfo.objects.filter(id=id)
        print(wb)
        if len(wb) == 0:
            resp = {"status": "1", "data": u"collect fail，no exited！"}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            wb = wb[0]
        old = Collect.objects.filter(user=user, pet=wb)
        if len(old) > 0:
            resp = {"status": "1", "data": u"collect fail，have colliected！"}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        collect = Collect()
        collect.user = user
        collect.pet = wb
        collect.save()
        resp = {"status": "0", "data": u"collect success"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except Exception as e:
        print(e)
        resp = {"status": "3", "data": u" error"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

@csrf_exempt
def delete_collect(request):
    try:
        user = request.user
        datas = json.loads(request.body)
        print(datas)
        id = datas["id"]
        print(id)
        old = Collect.objects.filter(id=id, user=user)
        if len(old) > 0:
            for i in old:
                i.delete()

        resp = {"status": "0", "data": u" Cancel successfully"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except Exception as e:
        print(e)
        resp = {"status": "3", "data": u" error"}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def my_adoption(request):
    user = request.user
    all_types = PetsType.objects.filter()
    try:
        if request.method == "GET":
            colls = Adoption.objects.filter(user=user)
            return render(request, "my_adoption.html", locals())
    except Exception as e:
        print(e)
        reason = "Error: System error"
        return render(request, "error.html", locals())

@csrf_exempt
def add_adoption(request):
    try:
        user = request.user
        datas = json.loads(request.body)
        print(datas)
        id = datas["id"]
        print(id)
        wb = PetsInfo.objects.filter(id=id)
        print(wb)
        if len(wb) == 0:
            resp = {"status": "1", "data": u"adopt fail，no exists！！"}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            wb = wb[0]
        old = Adoption.objects.filter(user=user, pet=wb)
        if len(old) > 0:
            resp = {"status": "1", "data": u"adopt fail，have adopted！"}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        collect = Adoption()
        collect.user = user
        collect.pet = wb
        collect.save()

        wb.status = "1"
        wb.save()

        resp = {"status": "0", "data": u"adoption success"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except Exception as e:
        print(e)
        resp = {"status": "3", "data": u" error"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

@csrf_exempt
def delete_adoption(request):
    try:
        user = request.user
        datas = json.loads(request.body)
        print(datas)
        id = datas["id"]
        print(id)
        old = Adoption.objects.filter(id=id, user=user)
        if len(old) > 0:
            for i in old:
                i.delete()
        resp = {"status": "0", "data": u"delete success"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except Exception as e:
        print(e)
        resp = {"status": "3", "data": u" error"}
        return HttpResponse(json.dumps(resp), content_type="application/json")



@login_required
@csrf_exempt
def detail(request):
    user = request.user
    try:
        if request.method == "GET":
            # all_types = PetsType.objects.filter()
            user = request.user
            id = request.GET.get("id", "")
            if id != "":
                pet = PetsInfo.objects.filter(id=id)
                if len(pet) > 0:
                    pet = pet[0]
                    return render(request, "detail.html", locals())
                else:
                    reason = "Sorry, it doesn't exist or has been deleted!!!"
                    return render(request, "error.html", locals())
            else:
                reason = "Sorry, it doesn't exist or has been deleted!!!"
                return render(request, "error.html", locals())

    except Exception as e:
        print(e)
        reason = "Sorry, the system error!" + str(e)
        return render(request, "error.html", locals())


@login_required
def my_info(request):
    try:
        user = request.user
        if request.method == "GET":
            collects = Collect.objects.filter(user=user)
            adopts = Adoption.objects.filter(user=user)
            return render(request, "my_info.html", locals())
        if request.method == "POST":
            username = request.POST.get("username", "")
            mobile = request.POST.get("mobile", "")
            email = request.POST.get("email", "")
            print(username)
            print(mobile)
            print(email)

            if mobile == "" or mobile == None or len(mobile) != 11:
                msg = "The mobile phone number cannot be empty, it must be 11 bits and the format is correct"
                return render(request, "my_info.html", locals())

            user.mobile = mobile
            user.email = email
            user.save()
            msg = "modify successful"
            return render(request, "my_info.html", locals())
    except Exception as e:
        print(e)
        msg = "System Error"
        return render(request, "my_info.html", locals())