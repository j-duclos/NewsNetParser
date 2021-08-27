# Default Django import
from dateutil.parser import parse
import time

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
import datetime
from simplecache.models import SimpleCache
from django.template.defaultfilters import slugify

# This class handles the scraping of HTML to get NewsNet titles, dates, and links
class NewsReleases():

    # Scrape the NewsNet digest for all article content
    @staticmethod
    def get_news_release_list(ward_number): 
 
        if ward_number == "1": 
            rss_feed = "https://public.govdelivery.com/topics/AZTUCSON_6/feed.rss"
        elif ward_number == "2":
            rss_feed = "https://public.govdelivery.com/topics/AZTUCSON_7/feed.rss"      
        elif ward_number == "3":
            rss_feed = "https://public.govdelivery.com/topics/AZTUCSON_11/feed.rss"      
        elif ward_number == "4":
            rss_feed = "https://public.govdelivery.com/topics/AZTUCSON_12/feed.rss"      
        elif ward_number == "5":
            rss_feed = "https://public.govdelivery.com/topics/AZTUCSON_13/feed.rss"      
        elif ward_number == "6":
            rss_feed = "https://public.govdelivery.com/topics/AZTUCSON_14/feed.rss"      
        else:
            rss_feed = "https://public.govdelivery.com/topics/AZTUCSON_9/feed.rss" 
            ward_number = "0"

        # Define the feed we will be pulling links from
        feed_page = requests.get(rss_feed)
        # Get the body of the request
        feed_html = feed_page.content

        # Create a dom tree to parse of our feed
        dom = etree.XML(feed_html)
        # Grab all of the link items - This returns all the urls from the rss feed:
        url_object = dom.xpath('//item/link/text()')

        # Grab all of the title items - This returns all the titles from the rss feed:
        title_object = dom.xpath('//item/title/text()')

        # Grab all of the date items - This returns the published date of each release: in this format: Tue, 05 Jan 2021 11:02:33 -0600
        date_object = dom.xpath('//item/pubDate/text()')

        # Initialize our list to store the links in
        url_list = list()

        # Look over the object containing our links
        for num, current_item in enumerate(url_object, start=0):
            # Initialize a list to store our values in
            current_item_list = list()
            # Get the URL
            # This returns the current news release url in the loop
            current_item_url = url_object[num]

            # Process the URL and get the token
            url_token = current_item_url.replace("https://content.govdelivery.com/accounts/AZTUCSON/bulletins/", "")
            current_item_list.append(url_token)
            current_item_list.append(title_object[num])

            # current_item_list - Returns url token and title of current news release

            # Returns the date of the news release as yyyy-mm-dd hh:mm:ss-06:00
            clean_date = parse(date_object[num], fuzzy=True)

            # Returns the url token, title, and date of the news release as yyyy-mm-dd hh:mm:ss-06:00
            current_item_list.append(clean_date.strftime("%B %d, %Y"))
            
            # Returns the url token, title, date of the news release as yyyy-mm-dd hh:mm:ss-06:00, and ward number
            current_item_list.append(ward_number)

            # Returns full list of all the url token, title, date of the news release as yyyy-mm-dd hh:mm:ss-06:00, and ward number
            # Add each link from the object to our list
            url_list.append(current_item_list)

        # Return our populated list
        return url_list

    @staticmethod
    def get_news_release(article):
        current_article = list()
        # Define the feed we will be pulling links from
        feed_page = requests.get("https://content.govdelivery.com/accounts/AZTUCSON/bulletins/" + article)
        # Get the body of the request
        feed_html = feed_page.content
        # Create a dom tree to parse of our HTML
        dom = etree.HTML(feed_html)

        # Get the date from the page
        article_title = dom.xpath('//h1[@class="bulletin_subject"]//text()')
        print("article_title")
        print(article_title)
        article_date = dom.xpath('//span[contains(@class, "dateline")]//text()')
        print("article_date")
        print(article_date)
        article_object = dom.xpath('//*[@id="bulletin_body"]')
        print("article_object")
        print(article_object)
        current_article_part = ""
        for article_part in article_object:
            this_part = etree.tostring(article_part, method='html', with_tail=False)
            current_article_part = this_part.decode("utf-8")

        current_article.append(article_title[0])
        current_article.append(article_date[0])
        current_article.append(current_article_part)

        print("current_article")
        print(current_article)
        
        return current_article
