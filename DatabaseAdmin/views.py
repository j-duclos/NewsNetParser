from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Article, NewsRelease
from NewsNetParser.models import NewsNetArticles
from NewsNetParser.views import *
#from django.contrib.auth.models import User
import os
from django.conf import settings
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView, 
    DeleteView
)
#from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 

"""
def updateList(request):
        print('test #1')
        # The RSS url we will be loading the newsletters from 
        news_net_feed_url = "https://public.govdelivery.com/topics/AZTUCSON_2/feed.rss"
        issue_count = 20  

        # Create an instance of the NewsNet Parser
        news_net_parser = NewsNetArticles()

        # returns model def __str__(self): from database
        context = {
            'articles': Article.objects.all().order_by('-date_sort')
        }

        print(context)
        # Fetch all the articles
        news_net_results = news_net_parser.get_news_net_list(news_net_feed_url, issue_count, False)
        
        for issue in news_net_results:
            for article in issue:
                #article[2] = date, article[0] = title, article[1] = content
                #Convert article date into a Datetime object Formatted as Stringv>> Date: Nov. 12, 2020
                month = article[2][6:9]
                day_str = article[2][10:13]
                day = day_str.replace(',', '') 
                day = int(day)
                year = int(article[2][14:19])
                this_date = (month + " " + str(day) + " " + str(year))
                date_time = datetime.strptime(this_date, '%b %d %Y')
                #Update Database with articles: title, date text, content, and converted date for ordering
                Article.objects.get_or_create(title = article[0], date_posted = article[2], content = article[1], date_sort = date_time)
        return context
        #return render(request, 'databaseadmin/home.html', context)
"""
  
class ArticleListView(ListView): 
    model = Article
    template_name = 'databaseadmin/home.html'
    context_object_name = 'articles'
    ordering = ['-date_sort']
    paginate_by = 5

    def __init__(self):
        self.model.updateList(self)

class ArticleArchivedListView(ListView): 
    model = Article
    template_name = 'databaseadmin/archived_home.html'
    context_object_name = 'articles'
    ordering = ['-date_sort']
    paginate_by = 5

    def __init__(self):
        self.model.updateArchivedList(self) 

class ArticleDetailView(DetailView): 
    model = Article
    template_name = 'databaseadmin/article_detail.html'

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'date_posted', 'content']
    template_name = 'databaseadmin/article_form.html'

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'date_posted', 'content']
    template_name = 'databaseadmin/article_form.html'

    def test_func(self):
        article = self.get_object()
        return True
        
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'databaseadmin/article_confirm_delete.html'
    # For Production
    #success_url = '/DatabaseAdmin/'
    # For Webdev2
    success_url = '/newsnet/DatabaseAdmin/'

    def test_func(self):
        article = self.get_object()
        return True


# News Releases for the Wards
class NewsReleaseListView(ListView): 
    model = NewsRelease
    template_name = 'databaseadmin/newsreleasehome.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']
    paginate_by = 5

    def __init__(self):
        self.model.updateList(self, 0)
        self.model.updateList(self, 1)
        self.model.updateList(self, 2)
        self.model.updateList(self, 3)
        self.model.updateList(self, 4)
        self.model.updateList(self, 5)
        self.model.updateList(self, 6)
"""
    def __init__(self):
        self.model.updateList(self)
        # Uncomment next line to activate Archived method; Keep commented otherwise
        #self.model.updateArchivedList(self) 

class ArticleArchivedListView(ListView): 
    model = Article
    template_name = 'databaseadmin/home.html'
    context_object_name = 'nr-articles'
    ordering = ['-date_sort']
    paginate_by = 5

    def __init__(self):
        self.model.updateArchivedList(self) 
"""