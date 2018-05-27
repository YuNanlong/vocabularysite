from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from accounts.models import User
from recitewords.models import WordBook
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import re

def my_validate_email(email):  
    from django.core.validators import validate_email  
    from django.core.exceptions import ValidationError  
    try:  
        validate_email(email)  
        return True  
    except ValidationError:  
        return False

username_pattern = re.compile(r'^[\w\.\+\-@]+$')

def signup(request):
    print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        raw_password_1 = request.POST['password1']
        raw_password_2 = request.POST['password2']
        email = request.POST['email']
        if re.match(username_pattern, username) is None:
            json_data = {'status': 'fail', 'field': 'username', 'error_message': '用户名格式错误'}
        elif len(username) < 6:
            json_data = {'status': 'fail', 'field': 'username', 'error_message': '用户名少于6位'}
        elif User.objects.filter(username=username).count() > 0:
            json_data = {'status': 'fail', 'field': 'username', 'error_message': '用户名已经被占用'}
        elif len(raw_password_1) < 6:
            json_data = {'status': 'fail', 'field': 'password1', 'error_message': '密码少于6位'}
        elif len(raw_password_2) < 6:
            json_data = {'status': 'fail', 'field': 'password2', 'error_message': '密码少于6位'}
        elif raw_password_1 != raw_password_2:
            json_data = {'status': 'fail', 'field': 'password2', 'error_message': '两次密码不一致'}
        elif my_validate_email(email) == False:
            json_data = {'status': 'fail', 'field': 'email', 'error_message': '邮箱格式错误'}
        elif User.objects.filter(email=email).count() > 0:
            json_data = {'status': 'fail', 'field': 'email', 'error_message': '邮箱已经被注册'}
        else:
            user = User.objects.create_user(username, email, raw_password_1)             
            user = authenticate(username=username, password=raw_password_1)
            login(request, user)
            json_data = {'status': 'success'}
        return JsonResponse(json_data)
    else:
        return render(request, 'signup.html')

def my_login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            json_data = {'status': 'success'}
        else:
            json_data = {'status': 'fail', 'field': 'password', 'error_message': '密码与用户名不匹配'}
        return JsonResponse(json_data)
    else:
        return render(request, 'login.html')  

def my_logout(request):
    logout(request)
    return HttpResponse("")

@login_required
def my_set(request):
    if request.method == 'POST':
        json_data = {}
        if 'personal-set' in request.POST:
            username = request.POST['username']
            raw_password_1 = request.POST['password1']
            raw_password_2 = request.POST['password2']
            email = request.POST['email']
            if username != request.user.username:
                if len(username) < 6:
                    json_data = {'status': 'fail', 'field': 'username', 'error_message': '用户名少于6位'}
                elif User.objects.filter(username=username).count() > 0:
                    json_data = {'status': 'fail', 'field': 'username', 'error_message': '用户名已经被占用'}
                else:    
                    request.user.username = username
                if json_data != {}:
                    return JsonResponse(json_data)
            if len(raw_password_1) > 0:
                if len(raw_password_1) < 6:
                    json_data = {'status': 'fail', 'field': 'password1', 'error_message': '密码少于6位'}
                elif raw_password_1 != raw_password_2:
                    json_data = {'status': 'fail', 'field': 'password2', 'error_message': '两次密码不一致'}
                else:
                    request.user.set_password(raw_password_1)
                if json_data != {}:
                    return JsonResponse(json_data)
            if email != request.user.email:
                if my_validate_email(email) == False:
                    json_data = {'status': 'fail', 'field': 'email', 'error_message': '邮箱格式错误'}
                elif User.objects.filter(email=email).count() > 0:
                    json_data = {'status': 'fail', 'field': 'email', 'error_message': '邮箱已经被注册'}
                else:
                    request.user.email = email
                if json_data != {}:
                    return JsonResponse(json_data)
            request.user.save()
            json_data = {'status': 'success'}
        elif 'learn-set' in request.POST:
            print(request.POST)
            # TODO 测试daily-task-amount为空的情况
            daily_task_amount = request.POST['daily-task-amount']
            exam_amount = request.POST['exam-amount']
            if len(daily_task_amount) == 0:
                json_data = {'status': 'fail', 'field': 'dailytaskamount', 'error_message': '每日单词量设置不能为空'}
            elif int(daily_task_amount) > 300:
                json_data = {'status': 'fail', 'field': 'dailytaskamount', 'error_message': '每日单词量不能超过300'}
            elif len(exam_amount) == 0:
                json_data = {'status': 'fail', 'field': 'examamount', 'error_message': '每次测试单词量设置不能为空'}
            else:
                json_data = {'status': 'success'}
        return JsonResponse(json_data)
    else:                
        return redirect('home')
