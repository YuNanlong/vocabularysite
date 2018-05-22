from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from recitewords.models import WordSet, WordBook

class User(AbstractUser):
    current_wordbook = models.ForeignKey(WordBook, null=True) # 当前正在学习的单词书
    daily_task_amount = models.IntegerField(default=0) # 每日任务单词总量
    learned_words = models.ManyToManyField(WordSet, related_name='user_learned_words', through='recitewords.LearnedWord') # 已学单词
    daily_task_words = models.ManyToManyField(WordSet, related_name='user_daily_task_words', through='recitewords.DailyTask') # 每日任务单词
    # TODO avatar = ProcessedImageField(upload_to=avatar_upload_path, default='avatar/default.jpg', verbose_name='头像', processors=[ResizeToFill(85,85)])

    def __str__(self):
        return self.username

    def remained_daily_task_amount(self):
        return self.dailytask_set.filter(is_finished=False).count()

    def mastered_words_amount(self):
        return self.learnedword_set.filter(mastery_degree=3).count()

    def need_to_learn(self):
        need_to_learn_list = []
        if self.current_wordbook:
            temp_learned_words_list = self.learnedword_set.filter(mastery_degree=3)
            learned_words_list = [i.word for i in temp_learned_words_list]
            current_wordset = self.current_wordbook.wordset_set.all()
            need_to_learn_list = [i for i in current_wordset if i not in learned_words_list]
        return need_to_learn_list

    def set_wordbook(self, wordbook):
        self.current_wordbook = wordbook
        self.save()

    def set_daily_task_amount(self, daily_task_amount):
        self.daily_task_amount = daily_task_amount
        self.save()    
