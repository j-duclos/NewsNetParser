from django.template import loader
import requests
from .models import NewsReleases
from django.http import HttpResponse


def index(request):
    # Create an instance of the NewsNet Parser
    news_release_parser = NewsReleases()

    # Fetch the articles - Returns all tokens, titles, dates, ward number '0'
    news_release_results = news_release_parser.get_news_release_list(0)  

    template = loader.get_template('newsreleases/index.html')
    
    context = {
        'news_release_results': news_release_results,
    }
    return HttpResponse(template.render(context, request))


def release(request):
    # Create an instance of the NewsNet Parser
    news_release_parser = NewsReleases()
    #article_name = requests.get('article')
    article_name = request.GET.get('article', None)
    # Fetch the articles
    news_release = news_release_parser.get_news_release(article_name) 

    template = loader.get_template('newsreleases/release.html')

    context = {
        'news_release': news_release,
    }

    return HttpResponse(template.render(context, request))
    
def ward(request):
    # Create an instance of the NewsNet Parser
    news_release_parser = NewsReleases()
    ward_number = request.GET.get('ward_number', None) 

    # Fetch the articles
    news_release_results = news_release_parser.get_news_release_list(ward_number)

    template = loader.get_template('newsreleases/ward.html')
    
    context = {
        'news_release_results': news_release_results,
    }
    return HttpResponse(template.render(context, request))

def ward2(request):
    # Create an instance of the NewsNet Parser
    news_release_parser = NewsReleases()
    #ward_number = request.GET.get('ward_number', None) 
    ward_number = '2'
    # Fetch the articles
    news_release_results = news_release_parser.get_news_release_list(ward_number)

    template = loader.get_template('newsreleases/ward.html')
    
    context = {
        'news_release_results': news_release_results,
    }
    print("Ward 2 Stuff")
    print(context)
    return HttpResponse(template.render(context, request))
