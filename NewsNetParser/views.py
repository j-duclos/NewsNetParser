from django.template import loader
from simplecache.models import SimpleCache
from NewsNetParser.models import NewsNetArticles 
from django.http import HttpResponse
from DatabaseAdmin import models
from django.templatetags.static import static
from django.conf import settings
import os
from pathlib import Path


# Create your views here. 
def index(request):
    # The RSS url we will be loading the newsletters from
    news_net_feed_url = "https://public.govdelivery.com/topics/AZTUCSON_2/feed.rss"

    issue_count = 10

    # Create an instance of the NewsNet Parser
    news_net_parser = NewsNetArticles()
    
    # Fetch the articles
    news_net_results = news_net_parser.get_news_net_list(news_net_feed_url, issue_count, False) 
    
    template = loader.get_template('newsnetparser/index.html')
    
    context = {
        'news_net_results': news_net_results, 
    }

    # To call DatabaseAdmin Refresh Function When Scrap is performed
    models.Article.updateList(request)

    return HttpResponse(template.render(context, request))


def newslist(request):
    # The RSS url we will be loading the newsletters from 
    news_net_feed_url = "https://public.govdelivery.com/topics/AZTUCSON_2/feed.rss"

    issue_count = 20
    
    # Create an instance of the NewsNet Parser
    news_net_parser = NewsNetArticles()
    
    # Fetch the articles
    news_net_results = news_net_parser.get_news_net_list(news_net_feed_url, issue_count, False)
    
    template = loader.get_template('newsnetparser/newslist.html')
    
    context = {
        'news_net_results': news_net_results, 
    }

    # To call DatabaseAdmin Refresh Function When Scrap is performed
    models.Article.updateList(request)

    return HttpResponse(template.render(context, request))


def recent(request):
    # The RSS url we will be loading the newsletters from 
    news_net_feed_url = "https://public.govdelivery.com/topics/AZTUCSON_2/feed.rss"

    issue_count = 10 
    
    # Create an instance of the NewsNet Parser
    news_net_parser = NewsNetArticles()
    
    # Fetch the articles
    news_net_results = news_net_parser.get_news_net_list(news_net_feed_url, issue_count, False) 
    
    template = loader.get_template('newsnetparser/recent.html')
    
    context = {
        'news_net_results': news_net_results, 
    }

    # To call DatabaseAdmin Refresh Function When Scrap is performed
    models.Article.updateList(request)

    return HttpResponse(template.render(context, request))


def latestlist(request):
    # The RSS url we will be loading the newsletters from 
    news_net_feed_url = "https://public.govdelivery.com/topics/AZTUCSON_2/feed.rss"

    issue_count = 'bulletin'
    
    # Create an instance of the NewsNet Parser
    news_net_parser = NewsNetArticles()
    
    # Fetch the articles
    news_net_results = news_net_parser.get_news_net_list(news_net_feed_url, issue_count, False) 
    
    template = loader.get_template('newsnetparser/latestlist.html')
    
    context = {
        'news_net_results': news_net_results, 
    }

    # To call DatabaseAdmin Refresh Function When Scrap is performed
    models.Article.updateList(request)

    return HttpResponse(template.render(context, request))


def clearcache(request):
    # Instantiate our cache
    news_net_cache = SimpleCache()
    
    # Provide a name for the cache object
    nn_cache_id = 'ALL'
    
    # Clear the cache
    news_net_cache.clear_cache(nn_cache_id)

    return HttpResponse('The NewsNet cache has been cleared.')