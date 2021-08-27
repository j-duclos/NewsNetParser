from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newslist', views.newslist, name='newslist'), 
    path('recent', views.recent, name='recent'),
    path('latestlist', views.latestlist, name='latestlist'),
    path('clearcache', views.clearcache, name='clearcache'), 
]