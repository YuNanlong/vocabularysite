from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from accounts.models import User
from recitewords.models import WordBook
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def my_validate_email(email):  
    from django.core.validators import validate_email  
    from django.core.exceptions import ValidationError  
    try:  
        validate_email(email)  
        return True  
    except ValidationError:  
        return False

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password_1 = request.POST['password1']
        raw_password_2 = request.POST['password2']
        email = request.POST['email']
        if len(username) < 6:
            return HttpResponse("<script>alert('用户名不能少于6个字符!'); window.location.href='/accounts/signup';</script>")
        if User.objects.filter(username=username).count() > 0:
            return HttpResponse("<script>alert('用户名已被占用!'); window.location.href='/accounts/signup';</script>")
        if len(raw_password_1) < 6:
            return HttpResponse("<script>alert('密码不能少于6个字符!'); window.location.href='/accounts/signup';</script>")
        if raw_password_1 != raw_password_2:
            return HttpResponse("<script>alert('两次输入的密码不一致!'); window.location.href='/accounts/signup';</script>")
        if my_validate_email(email) == False:
            return HttpResponse("<script>alert('请填写正确格式的邮箱!'); window.location.href='/accounts/signup';</script>")
        user = User.objects.create_user(username, email, raw_password_1)             
        user = authenticate(username=username, password=raw_password_1)
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'signup.html') 

def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('home')
        else:
            return HttpResponse("<script>alert('用户名或密码错误!'); window.location.href='/accounts/login';</script>")
    else:
        return render(request, 'login.html')  

def my_logout(request):
    logout(request)
    return redirect('login') 

@login_required
def my_set(request):
    if request.method == 'POST':
        if 'personal_setting' in request.POST:
            username = request.POST['username']
            raw_password_1 = request.POST['password1']
            raw_password_2 = request.POST['password2']
            email = request.POST['email']
            if username != request.user.username:
                if len(username) < 6:
                    return HttpResponse("<script>alert('用户名不能少于6个字符!'); window.location.href='/accounts/setting';</script>")
                if User.objects.filter(username=username).count() > 0:
                    return HttpResponse("<script>alert('用户名已被占用!'); window.location.href='/accounts/setting';</script>")
                request.user.username = username
            if len(raw_password_1) > 0:
                if len(raw_password_1) < 6:
                    return HttpResponse("<script>alert('密码不能少于6个字符!'); window.location.href='/accounts/setting';</script>")
                if raw_password_1 != raw_password_2:
                    return HttpResponse("<script>alert('两次输入的密码不一致!'); window.location.href='/accounts/setting';</script>")
                request.user.set_password(raw_password_1)
            if email != request.user.email:
                if my_validate_email(email) == False:
                    return HttpResponse("<script>alert('请填写正确格式的邮箱!'); window.location.href='/accounts/setting';</script>")
                request.user.email = email
            request.user.save()
        elif 'learn_setting' in request.POST:
            print(request.POST)
            # TODO 测试daily-task-amount为空的情况
            if 'daily-task-amount' in request.POST:
                daily_task_amount = request.POST['daily-task-amount']
                if int(daily_task_amount) <= 300:
                    request.user.set_daily_task_amount(int(daily_task_amount))
                else:
                    return HttpResponse("<script>alert('每日单词量不能超过300!'); window.location.href='/accounts/setting';</script>")
    return render(request, 'setting.html')
