from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.urls import reverse
from NewsNetParser.models import NewsNetArticles
from NewsReleases.models import NewsReleases
from datetime import datetime
import os
from django.conf import settings


class Article(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=255)
    date_posted = models.CharField(max_length=25)
    content = models.TextField()
    date_sort = models.DateTimeField(default=timezone.now)    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})     

    def updateList(self):
        # The RSS url we will be loading the newsletters from 
        news_net_feed_url = "https://public.govdelivery.com/topics/AZTUCSON_2/feed.rss"

        issue_count = 20  

        # Create an instance of the NewsNet Parser
        news_net_parser = NewsNetArticles()

        # returns model def __str__(self): from database
        context = {
            'articles': Article.objects.all().order_by('-date_sort')
        }

        # Fetch all the articles
        news_net_results = news_net_parser.get_news_net_list(news_net_feed_url, issue_count, False)

        for issue in news_net_results:
            for article in issue:
                try:
                    split_date = article[2].split(": ")
                    split_date.remove("Date")
                    for element in split_date:
                        date = element.split(" ")
                        month = date[0].split(".")
                        month = month[0]
                        day = date[1].split(",")
                        day = day[0]
                        year = date[2].replace("\xa0", "")

                        this_date = (month + " " + day + " " + year)

                        if len(month) > 3 or month == "May":
                            date_time = datetime.strptime(this_date, '%B %d %Y')
                        else:
                            date_time = datetime.strptime(this_date, '%b %d %Y')

                        #Update Database with articles: title, date text, content, and converted date for ordering
                        Article.objects.get_or_create(title = article[0], date_posted = article[2], content = article[1], date_sort = date_time)
                except Exception as e:
                    print("*******************there was an error*****************")
                    print(str(e))
                except RuntimeWarning as e:
                    print('*******************************')
                    print(str(e))
        return context


    def updateArchivedList(self):
        linelist = [line.rstrip('\n') for line in open(os.path.join(settings.BASE_DIR, 'newsnetarchive.txt'))]
        for line in linelist:
            news_net_feed = line
            #Use if "" are used
            #news_net_feed = line[1:-1]
            issue_count = 20  
            getArchivedList(self, news_net_feed, issue_count)


def getArchivedList(self, news_net_feed, issue_count):
    self.news_net_feed = news_net_feed
    self.issue_count = issue_count
    # Create an instance of the NewsNet Parser
    news_net_parser = NewsNetArticles()

    # returns model def __str__(self): from database
    context = {
        'articles': Article.objects.all().order_by('-date_sort')
    }
    print(news_net_feed)
    # Fetch all the articles
    news_net_results = news_net_parser.get_archived_news_net_list(news_net_feed, issue_count, False)
    for issue in news_net_results:
        for article in issue:
            try:
                split_date = article[2].split(": ")
                split_date.remove("Date")
                for element in split_date:
                    date = element.split(" ")
                    month = date[0]
                    day = date[1].split(",")
                    day = date[1][0]
                    year = date[2].replace("\xa0", "")
                    # year = date[2]

                    this_date = (month + " " + day + " " + year)

                    if len(month) > 3 or month == "May":
                        date_time = datetime.strptime(this_date, '%B %d %Y')
                    else:
                        date_time = datetime.strptime(this_date, '%b %d %Y')

                    #Update Database with articles: title, date text, content, and converted date for ordering
                    Article.objects.get_or_create(title = article[0], date_posted = article[2], content = article[1], date_sort = date_time)
            except Exception as e:
                print("*******************there was an error*****************")
                print(str(e))
                print(news_net_feed)

    return context
    #return render(request, 'databaseadmin/home.html', context)


class NewsRelease(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=255)
    date_posted = models.CharField(max_length=25)
    content = models.TextField()
    ward = models.CharField(max_length=2)
    #date_sort = models.DateTimeField(default=timezone.now)    

    def updateList(self, ward_number):
        self.ward_number = ward_number
        # Create an instance of the NewsNet Parser
        news_release_parser = NewsReleases()

        # returns model def __str__(self): from database
        context = {
            'newsrelease': NewsRelease.objects.all().order_by('-date_posted')
        }

        # Fetch all the articles
        news_release_results = news_release_parser.get_news_release_list(ward_number)
        print('news_release_results: ', news_release_results)

        for article in news_release_results:
            try:
                # article[0] = token, article[1] = title, article[2] = date,  article[3] = ward, 
                split_date = article[2].split(" ")
                month = split_date[0]
                day = split_date[1].split(",")
                day = day[0]
                year = split_date[2]

                this_date = (month + " " + day + " " + year)

                if len(month) > 3 or month == "May":
                    date_time = datetime.strptime(this_date, '%B %d %Y')
                else:
                    date_time = datetime.strptime(this_date, '%b %d %Y')

                # I may want to add this into the content 
                url = "https://content.govdelivery.com/accounts/AZTUCSON/bulletins/" + article[0]


                #Update Database with articles: title, date text, content, and converted date for ordering
                NewsRelease.objects.get_or_create(title = article[1], date_posted = date_time, content = " ", ward = ward_number)
                
            except Exception as e:
                print("*******************there was an error*****************")
                print(str(e))
        return context
        


"""
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('newsrelease-detail', kwargs={'pk': self.pk})     

    def updateList(self):
        # The RSS url we will be loading the newsletters from 
        #news_net_feed_url = "https://public.govdelivery.com/topics/AZTUCSON_2/feed.rss"
        #issue_count = 20  

        # Create an instance of the NewsNet Parser
        news_net_parser = NewsNetArticles()

        # returns model def __str__(self): from database
        context = {
            'articles': Article.objects.all().order_by('-date_sort')
        }

        # Fetch all the articles
        news_net_results = news_net_parser.get_news_net_list(news_net_feed_url, issue_count, False)

        for issue in news_net_results:
            for article in issue:
                try:
                    split_date = article[2].split(": ")
                    split_date.remove("Date")
                    for element in split_date:
                        date = element.split(" ")
                        month = date[0]
                        day = date[1].split(",")
                        day = date[1][0]
                        year = date[2].replace("\xa0", "")

                        this_date = (month + " " + day + " " + year)

                        if len(month) > 3 or month == "May":
                            date_time = datetime.strptime(this_date, '%B %d %Y')
                        else:
                            date_time = datetime.strptime(this_date, '%b %d %Y')

                        #Update Database with articles: title, date text, content, and converted date for ordering
                        Article.objects.get_or_create(title = article[0], date_posted = article[2], content = article[1], date_sort = date_time)
                except Exception as e:
                    print("*******************there was an error*****************")
                    print(str(e))
        return context


    def updateArchivedList(self):
        linelist = [line.rstrip('\n') for line in open(os.path.join(settings.BASE_DIR, 'newsnetarchive.txt'))]
        for line in linelist:
            news_net_feed = line
            #Use if "" are used
            #news_net_feed = line[1:-1]
            issue_count = 20  
            getArchivedList(self, news_net_feed, issue_count)


def getArchivedList(self, news_net_feed, issue_count):
    self.news_net_feed = news_net_feed
    self.issue_count = issue_count
    # Create an instance of the NewsNet Parser
    news_net_parser = NewsNetArticles()

    # returns model def __str__(self): from database
    context = {
        'articles': Article.objects.all().order_by('-date_sort')
    }
    print(news_net_feed)
    # Fetch all the articles
    news_net_results = news_net_parser.get_archived_news_net_list(news_net_feed, issue_count, False)
    for issue in news_net_results:
        for article in issue:
            try:
                split_date = article[2].split(": ")
                split_date.remove("Date")
                for element in split_date:
                    date = element.split(" ")
                    month = date[0]
                    day = date[1].split(",")
                    day = date[1][0]
                    year = date[2].replace("\xa0", "")
                # year = date[2]

                    this_date = (month + " " + day + " " + year)

                    if len(month) > 3 or month == "May":
                        date_time = datetime.strptime(this_date, '%B %d %Y')
                    else:
                        date_time = datetime.strptime(this_date, '%b %d %Y')

                    #Update Database with articles: title, date text, content, and converted date for ordering
                    Article.objects.get_or_create(title = article[0], date_posted = article[2], content = article[1], date_sort = date_time)
            except Exception as e:
                print("*******************there was an error*****************")
                print(str(e))
                print(news_net_feed)

    return context
    #return render(request, 'databaseadmin/home.html', context)

"""