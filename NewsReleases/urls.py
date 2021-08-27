from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('release', views.release, name='release'),
    path('ward', views.ward, name='ward'),
    path('ward2', views.ward2, name='ward2'),
]