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
        elif User.objects.filter(username=username).count() > 0:
            return HttpResponse("<script>alert('用户名已被占用!'); window.location.href='/accounts/signup';</script>")
        elif len(raw_password_1) < 6:
            return HttpResponse("<script>alert('密码不能少于6个字符!'); window.location.href='/accounts/signup';</script>")
        elif raw_password_1 != raw_password_2:
            return HttpResponse("<script>alert('两次输入的密码不一致!'); window.location.href='/accounts/signup';</script>")
        elif my_validate_email(email) == False:
            return HttpResponse("<script>alert('请填写正确格式的邮箱!'); window.location.href='/accounts/signup';</script>")
        else:
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
def reset_password(request):
    if request.method == 'POST':
        raw_password_1 = request.POST['password1']
        raw_password_2 = request.POST['password2']
        if len(raw_password_1) < 6:
            return HttpResponse("<script>alert('密码不能少于6个字符!'); window.location.href='/recite/reset_password';</script>")
        elif raw_password_1 != raw_password_2:
            return HttpResponse("<script>alert('两次输入的密码不一致!'); window.location.href='/recite/reset_password';</script>")
        else:
            request.user.set_password(raw_password_1)
            request.user.save()
            return redirect('home')
    else:
        return render(request, 'reset_password.html')    

@login_required
def learn_set(request):
    if request.method == 'POST':
        # TODO 测试daily-task-amount为空的情况
        if 'daily-task-amount' in request.POST:
            daily_task_amount = request.POST['daily-task-amount']
            if int(daily_task_amount) <= 300:
                request.user.set_daily_task_amount(daily_task_amount)
            else:
                return HttpResponse("<script>alert('每日单词量不能超过300!'); window.location.href='/accounts/learn_set';</script>")
        if 'wordbook' in request.POST:
            wordbook = get_object_or_404(WordBook, pk=request.POST['wordbook-id'])
            request.user.set_wordbook(wordbook)
            request.user.dailytask_set.delete()
        request.user.save()
        return redirect('home')
    else:
        wordbook_list = WordBook.objects.all()
        return render(request, 'learn_set.html', {'wordbook_list': wordbook_list})
