from django.urls import path
from . import views
from .views import (
    ArticleListView, 
    ArticleDetailView, 
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleArchivedListView,
    NewsReleaseListView,
)

urlpatterns = [
    #path('refresh/', views.updateList, name='update'),
    #path('', views.ArticleList, name='article-list'),
    path('', ArticleListView.as_view(), name='article-list'),
    path('getarchived/', ArticleArchivedListView.as_view(), name='archived-article-list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('newsrelease/', NewsReleaseListView.as_view(), name='news-release-list'),
    #path('user/<str:username>', UserArticleListView.as_view(), name='user-article'),
    
] 