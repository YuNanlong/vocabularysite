from django.contrib import admin
from .models import Word, WordBook, WordSet

class WordAdmin(admin.ModelAdmin):
    model = Word

class WordBookAdmin(admin.ModelAdmin):
    model = WordBook

class WordSetAdmin(admin.ModelAdmin):
    model = WordSet

admin.site.register(Word, WordAdmin)
admin.site.register(WordBook, WordBookAdmin)
admin.site.register(WordSet, WordSetAdmin)
