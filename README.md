# NewsNetParser

> Parses content from GovDelivery platform to create a presentable listing of newsletter content for the city website.

virtualenv env
source env/bin/activate
pip install mysqlclient
pip install django
pip install lxml
pip install requests

# Overview


https://github.com/tucsonaz/NewsNetParser	

These tools take RSS feeds from GovDelivery, parse the HTML page containing the newsletter item content, and produce various views. There is a very simple Drupal module that then takes those views and loads them into a Drupal block. 

This content exists on production (tucsonaz.gov) and the dev environment (devtucsonaz.central.tucsonaz.gov). The dev version of the drupal module should be pointing to my current dev version at devapps.city.tucsonaz.gov/webapp/ or the test version at testapp.city.tucsonaz.gov/webapp/. Note that I strongly encourage you to take advantage of the test environment here. When I moved the app from dev to test I encountered a huge number of configuration problems that saved me a lot of headaches when I deployed it to production.

The Drupal module is located in the main module folder and is titled “cot_newsnet” (again on both dev and prod). This module is pretty simple. It is just a collection of blocks that display the different views for the application. This is handled through PHP file_get_contents, so super low tech. The CSS in the module is also the primary CSS for the application. This makes emergency CSS edits a bit easier and means that the Django app itself is just raw HTML. 

**IMPORTANT BIT HERE**

There is a small daily maintenance task. Every day when the NewsNet is sent you need to make sure that all of the articles are showing up. Sometimes Robert will mess up the markup and you may need to make adjustments in GovDelivery to correct these problems. 

Go here and log in:
https://admin.govdelivery.com

Navigate to the following:
Topics -> NewsNet Daily Digest (not Newsnet for City Employees) -> Bulletins (menu on the right side) -> Sharing -> click on the title of the issue you need to edit -> make edits and hit save

Note that changes take a while (sometimes up to an hour) to show up on the bulletin page

Common problems are typically:
- Extra `<strong>` tags
- No `<p>` tags wrapping individual articles
- The dash after the title has an extra or missing space

The parser is super picky so it has to be exact.


# DatabaseAdmin

> Uploads the content NewsNetParser collected into a database table and displays them in a GUI for editors to view, modify, and create new. 
> Editors must have an account created to modify any data.

    /DatabaseAdmin/ returns the list of all NewsNet Articles in the database
    /DatabaseAdmin/getarchived runs a function that uses NewsNetParser to run against urls in the newsnetarchive.txt file (placed manually).  

    /DatabaseAdmin/newsrelease will return the Ward newsletters.  *** This is not done yet ***

# core/settings.py

> Be sure to add:
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        #BASE_DIR / "static",
        os.path.join(BASE_DIR, 'static'),
    ]

    #Added for crispy forms to use bootstrap 4
    CRISPY_TEMPLATE_PACK = 'bootstrap4' 

    # Redirect to home URL after login (Default redirects to /accounts/profile/)
    #LOGIN_REDIRECT_URL = '/'

    # This directory will differ on production
    LOGIN_REDIRECT_URL = '/newsnet/DatabaseAdmin/'

    #Changes auth login page 
    LOGIN_URL = 'login'
