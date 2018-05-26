from django.shortcuts import render, get_object_or_404, redirect
from recitewords.models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core import serializers 
import random

def home(request):
    if request.user.is_authenticated():
        DailyTask.init_daily_task(request.user)
        wordbook_list = WordBook.objects.all()
    return render(request, 'home.html', {'wordbook_list': wordbook_list})

@login_required
def show_wordbook_list(request):
    wordbook_list = WordBook.objects.all()
    return render(request, 'wordbook_list.html', {'wordbook_list': wordbook_list})

@login_required
def show_wordbook_detail(request):
    print(request.POST) # DEBUG
    print(request.GET) # DEBUG
    print(1) # DEBUG
    if request.method == 'POST':
        wordbook = get_object_or_404(WordBook, pk=request.POST['wordbook-id'])
        request.user.set_wordbook(wordbook)
        return redirect('home')
    else:
        wordbook = get_object_or_404(WordBook, pk=request.GET['wordbook-id'])
        return render(request, 'wordbook_detail.html', {'wordbook': wordbook})

def search_word(request):
    print(request.POST) # DEBUG
    print(request.GET) # DEBUG
    if request.method == 'POST':
        try:
            result = Word.objects.get(spelling=request.POST['searching-word'])
        except:
            result = None
        print(result)
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
                json_data = {'word_spelling': None, 'task_id': None, 'word_meaning': None}
            else:
                json_data = {'word_spelling': next_word.word.word.spelling, 'task_id': next_word.task_id, 'word_meaning': next_word.word.word.meaning}
            print(json_data) # DEBUG
            return JsonResponse(json_data)
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
                json_data = {'word_spelling': None, 'task_id': None, 'word_meaning': None, 'proportion': 0}
            else:
                total = request.user.daily_task_words.count()
                remained = request.user.remained_daily_task_amount()
                proportion = remained / total
                json_data = {'word_spelling': next_word.word.word.spelling, 'task_id': next_word.task_id, 'word_meaning': next_word.word.word.meaning, 'proportion': proportion}
            return JsonResponse(json_data)
        else:   
            return redirect('home')
    else:
        DailyTask.init_daily_task(request.user)
        try:
            word = DailyTask.objects.get(user=request.user, task_id=1)
            if word.is_finished == True:
                word = word.get_next_word()
            print(word) # DEBUG
            if word is None:
                return HttpResponse("<script>alert('您已经完成今日学习任务!'); window.location.href='/recite/home';</script>")
            else:
                total = request.user.daily_task_words.count()
                remained = request.user.remained_daily_task_amount()
                remained_proportion = '%.0f%%' % (remained / total * 100)
                finished_proportion = '%.0f%%' % (100 - remained / total * 100)
                return render(request, 'recite_word.html', {'word': word, 'finished_proportion': finished_proportion, 'remained_proportion': remained_proportion})
        except:
            return HttpResponse("<script>alert('尚未选择单词书!'); window.location.href='/accounts/setting';</script>")

@login_required
def exam_set(request):
    print(request.POST) # DEBUG
    print(request.GET) # DEBUG
    if request.method == 'POST':
        request.user.exam_amount = int(request.POST['exam-amount'])
        request.user.save()
        return redirect('exam')
    else:
        return render(request, 'exam_set.html')

@login_required
def exam(request):
    if request.method == 'POST':
        print(request.POST) # DEBUG
        learned_word = get_object_or_404(LearnedWord, pk=request.POST['id'])
        if learned_word.mastery_degree > 0:
            learned_word.mastery_degree -= 1
            learned_word.save()
        return HttpResponse("")
    else:
        if 'get_exam_words' in request.GET:
            candidate_word_set = list(LearnedWord.objects.filter(user=request.user))
            word_list = []
            id_list = []
            if len(candidate_word_set) <= request.user.exam_amount:
                for i in candidate_word_set:
                    word_list.append(i.word.word.spelling)
                    id_list.append(i.id)
            else:
                exam_word_set = random.sample(candidate_word_set, request.user.exam_amount)
                for i in exam_word_set:
                    word_list.append(i.word.word.spelling)
                    id_list.append(i.id)
            json_data = {'word_list': word_list, 'id_list': id_list}
            return JsonResponse(json_data)
        else:
            return render(request, 'exam.html')
