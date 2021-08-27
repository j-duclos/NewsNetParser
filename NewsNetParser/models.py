# Default Django import
from django.db import models

# Imports for Simple Cache
from django.utils import timezone
from django.db import DatabaseError, transaction
from django.core.exceptions import ObjectDoesNotExist 

# Imports for NewsNetParser
from lxml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import re
import requests
from simplecache.models import SimpleCache
from django.template.defaultfilters import slugify


# This class handles the scraping of HTML to get NewsNet titles, dates, and links 
class NewsNetArticles:

    # Initialize the article counters so we can limit articles displayed
    article_count = 0

    # Scrape the NewsNet digest for all article content
    def get_article_content(self, bulletin_url, article_limit): 
        # Check to see if we are counting articles
        if article_limit == 'bulletin':
            # We need to make sure a default article limit is set when we start our count
            article_limit = 10
            # Set our article count to a string to start the count
            articles_in_bulletin = 'bulletin'
        else:
            # Since we aren't doing an article count and we need to define the var, we just set it to the article limit
            articles_in_bulletin = article_limit
      
        # Check to see if we have exceeded the article limit passed in yet
        if self.article_count <= article_limit:
            # using a get request load the bulletin from the URL
            news_net_page = requests.get(bulletin_url)
            # Get the content section/HTML of the get request
            news_net_html = news_net_page.content
            # Create a dom tree to parse of our HTML 
            dom = etree.HTML(news_net_html)
            # Get the date from the page
            date_object = dom.xpath('//p/strong//text()')
            # Get all titles from the page
            # Note that this assumes the only bold text follows an H3 and a p tag and is wrapped in a strong tag
            titles_object = dom.xpath('//h3/following-sibling::p/strong//text()')
            article_content_object = dom.xpath('//h3/following-sibling::p')
            # Check to see if we need to do an article count
            if articles_in_bulletin == 'bulletin':
                # Count our articles and subtract one since on the first pass we will already be in the loop
                article_limit = len(titles_object) - 1

            # Initialize our return variable
            title_output = list()

            # Loop over the titles that have been returned from our scrape
            for current_article in article_content_object:

                # Create a list to store the values in
                article_details = list()

                current_article = tostring(current_article, 'utf-8')

                # If we have not exceeded the article limit, continue adding titles
                if self.article_count <= article_limit:

                    article_dom = etree.fromstring(current_article)
                    current_article_title = article_dom.xpath('//strong/text()')
                    current_article_dom = article_dom.xpath('//*')
                    clean_article = ''

                    for part_num, current_part in enumerate(current_article_dom, start=0):

                        try:
                            current_title = current_article_title[0]
                        except IndexError:
                            current_title = 0

                        if (part_num == 0) and (current_title != 0):
                            current_part_dom = etree.fromstring(tostring(current_part, 'utf-8'))
                            clean_article = self.clean_article(current_part_dom)
                            article_details.append(current_article_title[0])
                            article_details.append(clean_article) 
                            article_details.append(date_object[0]) 
                            article_details.append(bulletin_url)
                            article_details.append(self.article_count)
                            article_details.append(slugify(current_article_title[0]))
                            article_details.append(articles_in_bulletin) 
                            
                            # Increment our article count 
                            self.article_count += 1

                    if clean_article != '':
                        title_output.append(article_details)
                    
                else:
                    # If our article limit has been reached, stop processing articles and exit the for each loop
                    break
                        
            # Return the list of titles and dates
            return title_output
        else:
            # If we reached our limit before performing a new scrape just return an empty string
            return ""   

    @staticmethod
    def clean_article(current_article):
        current_article = tostring(current_article, "utf-8")
        current_article = current_article.decode("utf-8")
        current_article = re.sub("((<p)(.*)(<strong>)()(.*?)(<\/strong>))", "", current_article)
        current_article = re.sub("^( - )", "", current_article)
        current_article = re.sub("^( – )", "", current_article)
        current_article = re.sub("<\/p>$", "", current_article)
        return current_article

    # Get the list of links from the RSS feed
    @staticmethod
    def get_newsletters(rss_feed):
        # Define the feed we will be pulling links from
        feed_page = requests.get(rss_feed)
        # Get the body of the request
        feed_html = feed_page.content

        # Create a dom tree to parse of our feed
        dom = etree.XML(feed_html)
        # Grab all of the link items
        url_object = dom.xpath('//item/link/text()')

        # Initialize our list to store the links in
        url_list = list()

        # Look over the object containing our links
        for feed_bulletin_url in url_object:
            # Add each link from the object to our list
            url_list.append(feed_bulletin_url)

        # Return our populated list
        return url_list

    @staticmethod
    def get_news_net_list(feed_url, issue_count, clear_cache=False):
        # Instantiate our cache
        news_net_cache = SimpleCache()
        
        # Check to see if we are trying to display a full bulletin or not
        if issue_count != 'bulletin':
            # Since our count starts at zero, we adjust the count passed into the tempalte
            issue_count = issue_count - 1
        else:
            # This is a bulletin, so we need to pass the string to trigger an article count
            issue_count = 'bulletin'
        
        # Provide a name for the cache object
        nn_cache_id = 'NewsNetCacheID' + str(issue_count)
        # Make sure we are defaulting to assuming that there is no cache
        nn_cache_check = False

        # Check to see if a forced cache clear has been requested
        if clear_cache:
            # Clear the cache
            news_net_cache.clear_cache(nn_cache_id)
        else:
            # Check to see if the cache has already been set
            nn_cache_check = news_net_cache.check_cache(nn_cache_id)

        # If the cache is not set, we create it, otherwise we load it
        if nn_cache_check is False:

            # instantiate our NewsNet Article processor
            get_articles = NewsNetArticles()
            # Pass the URL in to grab the feed items we will be parsing
            feed_list = get_articles.get_newsletters(feed_url)

            # initialize a variable to store our list of articles in
            nn_cache_value = list()
            # Loop over the individual URLs
            for issue_url in feed_list:
                # For each URL we are grabbing the title which include the date of the article below it
                nn_cache_value.append(get_articles.get_article_content(issue_url, issue_count))

            # Set the duration of our cache
            nn_cache_duration = timezone.now() + timezone.timedelta(hours=1)
           
            # Clean up our list, removing any empty fields before adding it to the cache
            while "" in nn_cache_value:
                nn_cache_value.remove("") 
           
            # Once our content has been parsed we add it to the cache
            news_net_cache.set_cache(nn_cache_id, nn_cache_duration, nn_cache_value)
        else:
            # If the item exists in cache, we need to load it
            nn_cache_result = news_net_cache.get_cache(nn_cache_id)
            # Get the value from our result
            nn_cache_value = eval(nn_cache_result.cache_value)
            
            # Clean up our list, removing any empty fields before adding it to the cache
            while "" in nn_cache_value:
                nn_cache_value.remove("") 

        return nn_cache_value

    @staticmethod
    def get_archived_news_net_list(feed_url, issue_count, clear_cache=False):
        # Instantiate our cache
        get_articles = NewsNetArticles()
        nn_cache_value = list()
        nn_cache_value.append(get_articles.get_article_content(feed_url, issue_count))

        while "" in nn_cache_value:
            nn_cache_value.remove("")
        return nn_cache_value