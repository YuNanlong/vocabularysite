from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^login', views.my_login, name='login'),
    url(r'^logout', views.my_logout, name='logout'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^setting', views.my_set, name='setting'),
]
