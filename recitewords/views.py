from django.shortcuts import render, get_object_or_404, redirect
from recitewords.models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def home(request):
    DailyTask.init_daily_task(request.user)
    return render(request, 'home.html')

@login_required
def show_wordbook_list(request):
    wordbook_list = WordBook.objects.all()
    return render(request, 'wordbook_list.html', {'wordbook_list': wordbook_list})

@login_required
def show_wordbook_detail(request):
    if request.method == 'POST':
        wordbook = get_object_or_404(WordBook, pk=request.POST['wordbook-id'])
        request.user.set_wordbook(wordbook)
        return redirect('home')
    else:
        wordbook = get_object_or_404(WordBook, pk=request.GET['wordbook-id'])
        return render(request, 'wordbook_detail.html', {'wordbook': wordbook})

@login_required
def search_word(request):
    if request.method == 'POST':
        try:
            result = Word.objects.get(spelling=request.POST['searching-word'])
        except:
            result = None
        return render(request, 'search_word.html', {'is_search': True, 'result': result})
    else:
        return render(request, 'search_word.html', {'is_search': False})

@login_required
def recite_word(request):
    if request.method == 'POST':
        print(request.POST) #DEBUG
        if 'add_to_favor' in request.POST:
            return redirect('home')
        elif 'next-word' in request.POST:
            task_id = request.POST['task-id']
            current_word = get_object_or_404(DailyTask, user=request.user, task_id=task_id)
            next_word = current_word.get_next_word()
            if next_word is None:
                return HttpResponse("<script>alert('您已经完成今日学习任务!'); window.location.href='/recite/home';</script>")
            else:
                return render(request, 'recite_word.html', {'word': next_word})
        elif 'know' in request.POST:
            task_id = request.POST['task-id']
            current_word = get_object_or_404(DailyTask, user=request.user, task_id=task_id)
            current_word.is_finished = True
            current_word.save()
            learned_word = LearnedWord.objects.get_or_create(user=request.user, word=current_word.word)
            learned_word[0].mastery_degree += 1
            learned_word[0].save()
            next_word = current_word.get_next_word()
            if next_word is None:
                return HttpResponse("<script>alert('您已经完成今日学习任务!'); window.location.href='/recite/home';</script>")
            else:
                return render(request, 'recite_word.html', {'word': next_word})
        elif 'unknow' in request.POST:
            task_id = request.POST['task-id']
            current_word = get_object_or_404(DailyTask, user=request.user, task_id=task_id)                
            return render(request, 'word_detail.html', {'word': current_word})
        else:   
            return redirect('home')
    else:
        DailyTask.init_daily_task(request.user)
        try:
            word = DailyTask.objects.get(user=request.user, task_id=1)
            if word.is_finished == True:
                word = word.get_next_word()
            print(word)
            if word is None:
                return HttpResponse("<script>alert('您已经完成今日学习任务!'); window.location.href='/recite/home';</script>")
            else:
                return render(request, 'recite_word.html', {'word': word})
        except:
            return HttpResponse("<script>alert('尚未选择单词书!'); window.location.href='/accounts/setting';</script>")

