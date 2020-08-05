from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os
import datetime
def index(request):
    return render(request, 'index.html', {})

def chkusrname(request):
    if request.method == 'GET':
        username = request.GET.get('rusername')
        user = User()
        if User.objects.filter(username=username).count()==0:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
@csrf_exempt
def registerForm(request):
    if request.method == 'POST':
        username = request.POST.get('rusername')
        password = request.POST.get('rpassword')
        user = authenticate(username=username, password=password)
        if user is None:
            user = User()
            if User.objects.filter(username=username).count()==0:
                User.objects.create_user(username, '', password)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False,"reason":"Username Already Exists !!!!!"})
    return JsonResponse({'success': False,"reason":"Sorry something went Worng !!!!!"})
@csrf_exempt
def loginForm(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                request.session['username']=username
                login(request, user)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False,"reason":"Sorry something went Worng !!!!!"})

@login_required(login_url='/')
def success(request):
    return render(request, 'main_page.html', {})

def signout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def savedata(request):
    if request.method == 'POST':
        username=request.session.get('username')
        TableData=request.POST.get('tabledata')
        user=User.objects.get(username=username)
        x = date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date=str(date).replace(' ','_')
        date=str(date).replace(':','-')
        if request.POST.get('update')=="update":
            date=request.POST.get('date')
            filedata = userfilepaths.objects.get(user_id=user.id,date=date)
            f = open(filedata.filepath, "w")
            f.write(TableData)
            f.close()
            filedata.date=x
            filedata.save()
            return JsonResponse({'success': True,'date':x})
        else:
            filename="media/records/"+username+"_"+date+".html"
            f = open(filename,"w+")
            f.write(TableData)
            f.close()
            filedata=userfilepaths()
            filedata.user_id=user.id
            filedata.filepath=filename
            filedata.date=x
            filedata.save()
            return JsonResponse({'success': True,'date':x})


def loadata(request):
    if request.method == 'GET':
        date = request.GET.get('selectval')
        filedata = userfilepaths.objects.get(date=date)
        filepath=filedata.filepath
        f = open(filepath,"r")
        tabledata=f.read()
        return JsonResponse({'success': True,'data':tabledata})

@csrf_exempt
def deldata(request):
    try:
        if request.method == 'POST':
            filedata = userfilepaths.objects.get(date=request.POST.get('date'))
            filepath = filedata.filepath
            os.remove(filepath)
            userfilepaths.objects.filter(filepath=filepath).delete()
            return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})
    

def ajaxdropdown(request):
    if request.method == 'GET':
        username = request.session.get('username')
        date=" "
        if request.GET.get('date') != None:
            date = request.GET.get('date')
        user=User.objects.get(username=username)
        filedata = userfilepaths.objects.filter(user_id=user.id).order_by("-date")
        return render(request,'include/dropdown.html',{'filedate':filedata,'date':date})
