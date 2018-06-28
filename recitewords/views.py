from django.shortcuts import render, get_object_or_404, redirect
from recitewords.models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core import serializers 
import random

def home(request):
    wordbook_list = None
    if request.user.is_authenticated():
        DailyTask.init_daily_task(request.user)
        wordbook_list = WordBook.objects.all()
    return render(request, 'home.html', {'wordbook_list': wordbook_list})

def show_wordbook_list(request):
    if request.user.is_authenticated() == False:
        return HttpResponse("<script>alert('请先登录'); window.location.href='/recite/home';</script>")
    wordbook_list = WordBook.objects.all()
    for wb in wordbook_list:
        wb.total_mastered = LearnedWord.objects.filter(word__wordbook=wb, user=request.user, mastery_degree=3).count()
        wb.total_learned = LearnedWord.objects.filter(word__wordbook=wb, user=request.user).count()
        wb.learned_percent = round(wb.total_learned / wb.words.count() * 100, 2)
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

def recite_word(request):
    if request.user.is_authenticated() == False:
        return HttpResponse("<script>alert('请先登录'); window.location.href='/recite/home';</script>")
    if request.method == 'POST':
        if 'add_to_favor' in request.POST:
            return redirect('home')
        elif 'next-word' in request.POST:
            task_id = request.POST['task-id']
            current_word = get_object_or_404(DailyTask, user=request.user, task_id=task_id)
            next_word = current_word.get_next_word()
            if next_word is None:
                json_data = {'word_spelling': None, 'task_id': None, 'word_meaning': None}
            else:
                try:
                    request.user.favor_words.get(pk=next_word.word.id)
                    is_favored = True
                except:
                    is_favored = False
                json_data = {'word_spelling': next_word.word.word.spelling, 'task_id': next_word.task_id, 'word_meaning': next_word.word.word.meaning, 'is_favored': is_favored}
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
                try:
                    request.user.favor_words.get(pk=next_word.word.id)
                    is_favored = True
                except:
                    is_favored = False
                json_data = {'word_spelling': next_word.word.word.spelling, 'task_id': next_word.task_id, 'word_meaning': next_word.word.word.meaning, 'proportion': proportion, 'is_favored': is_favored}
            return JsonResponse(json_data)
        else:   
            return redirect('home')
    else:
        if request.user.daily_task_amount == 0:
            return HttpResponse("<script>alert('请先设置每日学习单词量'); window.location.href='/recite/home';</script>")
        DailyTask.init_daily_task(request.user)
        try:
            word = DailyTask.objects.get(user=request.user, task_id=1)
            if word.is_finished == True:
                word = word.get_next_word()
            if word is None:
                return HttpResponse("<script>alert('您已经完成今日学习任务!'); window.location.href='/recite/home';</script>")
            else:
                total = request.user.daily_task_words.count()
                remained = request.user.remained_daily_task_amount()
                remained_proportion = '%.0f%%' % (remained / total * 100)
                finished_proportion = '%.0f%%' % (100 - remained / total * 100)
                try:
                    request.user.favor_words.get(pk=word.word.id)
                    is_favored = True
                except:
                    is_favored = False
                return render(request, 'recite_word.html', {'word': word, 'finished_proportion': finished_proportion, 'remained_proportion': remained_proportion, 'is_favored': is_favored})
        except:
            return HttpResponse("<script>alert('尚未选择单词书!'); window.location.href='/recite/home';</script>")

def exam(request):
    if request.user.is_authenticated() == False:
        return HttpResponse("<script>alert('请先登录'); window.location.href='/recite/home';</script>")
    if request.method == 'POST':
        learned_word = get_object_or_404(LearnedWord, pk=request.POST['id'])
        if learned_word.mastery_degree > 0:
            learned_word.mastery_degree -= 1
            learned_word.save()
        return HttpResponse("")
    else:
        if 'get_exam_words' in request.GET:
            all_word_set = list(request.user.current_wordbook.wordset_set.all())
            candidate_word_set = list(LearnedWord.objects.filter(user=request.user))
            random.shuffle(candidate_word_set)
            word_list = []
            meaning_list = []
            id_list = []
            error_word_list = []
            if request.user.exam_amount == 0:
                return JsonResponse({'exam_amount': 0})
            if len(candidate_word_set) <= request.user.exam_amount:
                for i in candidate_word_set:
                    word_list.append(i.word.word.spelling)
                    meaning_list.append(i.word.word.meaning)
                    id_list.append(i.id)
            else:
                exam_word_set = random.sample(candidate_word_set, request.user.exam_amount)
                for i in exam_word_set:
                    word_list.append(i.word.word.spelling)
                    meaning_list.append(i.word.word.meaning)
                    id_list.append(i.id)
            iter_times = 30
            if request.user.exam_amount > 30:
                iter_times = request.user.exam_amount
            for i in range(iter_times):
                while True:
                    error_word = random.sample(all_word_set, 1)[0]
                    if error_word.word.id in id_list:
                        continue
                    error_word_list.append(error_word.word.meaning)
                    break
            json_data = {'exam_amount': request.user.exam_amount, 'word_list': word_list, 'id_list': id_list, 'meaning_list': meaning_list, 'error_word_list': error_word_list}
            return JsonResponse(json_data)
        else:
            return render(request, 'exam.html')

def favor_word(request):
    if request.user.is_authenticated() == False:
        return HttpResponse("<script>alert('请先登录'); window.location.href='/recite/home';</script>")
    if request.method == 'POST':
        word = get_object_or_404(DailyTask, user=request.user, task_id=int(request.POST['task-id'])).word
        try:
            request.user.favor_words.get(pk=word.id)
            request.user.favor_words.remove(word)
        except:
            request.user.favor_words.add(word)
        return JsonResponse({})
    else:
        if 'id' in request.GET.keys():
            id = int(request.GET['id'])
            word = get_object_or_404(WordSet, pk=id)
            request.user.favor_words.remove(word)
            return redirect('favor_word')
        favor_word_list = request.user.favor_words.all()
        return render(request, 'favor_word.html', {'favor_word_list': favor_word_list})

def exam_result(request):
    result = round(float(request.GET['result']) * 100)
    return render(request, 'exam_result.html', {'result': result})
