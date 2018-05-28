from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import datetime
import time

def bookfront_upload_path(instance, filename):
    return '/'.join(['bookfront', time.strftime('%y%m%d%H%M%S')]) + '.jpg'

# 单词
class Word(models.Model):
    spelling = models.CharField(max_length=255, unique=True, blank=False)
    meaning = models.TextField() # 单词详细释义
    past_tense = models.CharField(max_length=64)
    past_priciple = models.CharField(max_length=64)
    present_progressive = models.CharField(max_length=64)
    plurality = models.CharField(max_length=64)
    example = models.TextField()

    def __str__(self):
        return self.spelling

# 单词书
class WordBook(models.Model):
    name = models.CharField(max_length=128, unique=True, blank=False) # 单词书名称
    description = models.TextField() # 单词书简介
    front_image = models.ImageField(upload_to=bookfront_upload_path, default='bookfront/default.jpg') # 单词书封面
    words = models.ManyToManyField(Word, through='WordSet') # 单词书的单词集

    def __str__(self):
        return self.name

# 单词集
class WordSet(models.Model):
    wordbook = models.ForeignKey(WordBook) # 单词所属单词书
    word = models.ForeignKey(Word) # 单词

    def __str__(self):
        return self.wordbook.name + ' : ' + self.word.spelling

# 已学单词
class LearnedWord(models.Model):
    user = models.ForeignKey('accounts.User') # 用户
    word = models.ForeignKey(WordSet) # 单词
    mastery_degree = models.IntegerField(default=0, blank=False) # 掌握程度

# 学习进度记录
class DailyProgress(models.Model):
    user = models.ForeignKey('accounts.User') # 用户
    word = models.ForeignKey(WordSet) # 单词
    learn_date = models.DateField() # 学习时间

# 每日学习任务
class DailyTask(models.Model):
    user = models.ForeignKey('accounts.User') # 用户
    word = models.ForeignKey(WordSet) # 单词
    update_date = models.DateField() # 学习任务更新时间
    is_finished = models.BooleanField(default=False) # 今日是否完成学习
    task_id = models.IntegerField(null=True) # 单词在每日学习任务中的编号

    @classmethod
    def create(cls, user, word, update_date, is_finished, task_id):
        daily_task = cls(user=user, word=word, update_date=update_date, is_finished=is_finished, task_id=task_id)
        return daily_task

    def get_next_word(self):
        task_id = self.task_id
        while True:
            if task_id == self.user.daily_task_words.count():
                task_id = 1
            else:
                task_id += 1
            try:
                next_word = DailyTask.objects.get(user=self.user, update_date=datetime.date.today(), task_id=task_id)
                if next_word.is_finished == False:
                    return next_word
                elif self.task_id == next_word.task_id:
                    return None
                else:
                    continue
            except:
                return None

    @staticmethod
    def init_daily_task(user):
        if len(DailyTask.objects.filter(user=user, update_date=datetime.date.today())) < 1:
            past_task = list(DailyTask.objects.filter(user=user))
            task_id = 1
            for i in past_task:
                if i.is_finished == True:
                    i.delete()
                else:
                    if task_id <= user.daily_task_amount:
                        i.task_id = task_id
                        i.update_date = datetime.date.today()
                        i.save()
                        task_id += 1
                    else:
                        i.delete() # TODO 测试每日单词量减少至少于之前未完成的总量的情况
            print(user.daily_task_amount)
            for i in user.need_to_learn():
                if task_id <= user.daily_task_amount:
                    try:
                        DailyTask.objects.get(user=user, word=i)
                    except:
                        daily_task = DailyTask.create(user, i, datetime.date.today(), False, task_id)
                        daily_task.save()
                        task_id += 1
                else:
                    break
