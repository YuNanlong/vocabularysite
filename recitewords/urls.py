from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^home', views.home, name='home'),
    url(r'^wordbook_list', views.show_wordbook_list, name='wordbook_list'),
    url(r'^wordbook_detail', views.show_wordbook_detail, name='wordbook_detail'),
    url(r'^search_word', views.search_word, name='search_word'),
    url(r'^recite_word', views.recite_word, name='recite_word'),
]
