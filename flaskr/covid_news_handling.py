'''
    The tasks of this file are as follows:
        - update the news
        - fetches the news with a specified url along with parameters found in the config file
        - schedules news updates
        - stores the title of deleted news articles
        - removes news articles
'''



import json
import logging
import time
import requests



from flaskr import shared_config_file
from flaskr import shared_scheduler
from flaskr import updates_handler



#dictionary containing keys for the parameters required to access the news from the url

news_info = {
    "apiKey": "apiKey",
    "from": "from",
    "language": "language",
    "pageSize": "pageSize",
    "sortBy": "sortBy",
    "terms": "terms"
}



#list of news articles

NEWS_ARTICLES = []

#list of the titles of deleted news articles

DELETED_NEWS_ARTICLES_TITLES = []



def update_news(title_of_update = ""):
    '''
    function which calls other functions in order to update the news
    '''

    global NEWS_ARTICLES

    news_info["apiKey"] = shared_config_file.data["news"]["apiKey"]
    news_info["from"] = shared_config_file.data["news"]["from"]
    news_info["language"] = shared_config_file.data["news"]["language"]
    news_info["pageSize"] = shared_config_file.data["news"]["pageSize"]
    news_info["sortBy"] = shared_config_file.data["news"]["sortBy"]
    news_info["terms"] = shared_config_file.data["news"]["covidTerms"]

    #call function to get news

    NEWS_ARTICLES = news_API_request(news_info["terms"])

    #call function to remove news article

    remove_news_article()

    #call function to find update

    update = updates_handler.find_update(title_of_update)

    #if the update is found

    if update is not None:

    #if the value for the key 'repeating' is true, then schedule another update

        if update["repeating"]:

            schedule_news_updates(60*60*24, title_of_update)

        #if not then delete the update from the list of existing updates

        else:

            updates_handler.delete_updates(title_of_update)



def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    '''
    function to get news articles from website
    '''

    terms_to_search = ""

    #split into a new item in the list everytime a space is seen
    #then loop through each element in list

    for element in list(map(str, covid_terms.split())):

    #if the element is the first element, no need to add ' OR '

        if terms_to_search == "":

        #just add element to list

            terms_to_search += element
        else:

        #add ' OR ' followed by element

            terms_to_search += " OR " + element

    parameters = {
        "apiKey": news_info["apiKey"],
        "from": news_info["from"],
        "language": news_info["language"],
        "pageSize": news_info["pageSize"],
        "sortBy": news_info["sortBy"],
        "q": terms_to_search
    }

    url = shared_config_file.data["news"]["apiUrl"]

    try:

    #gets data from the url via a 'GET' request

        data = requests.get(url, params = parameters)

        #assign the value associated to the "articles" key to be the news

        news = json.loads(data.text)["articles"]
        logging.info("News fetched successfully")

    #cannot connect to the server

    except requests.exceptions.ConnectionError as error:

        logging.error("Unable to fetch news articles: %s", error)

    return news



def schedule_news_updates(update_interval, update_name):
    '''
    schedule the update
    '''

    event = shared_scheduler.scheduler.enterabs(
        time.time()+update_interval, 1, update_news, (update_name,))

    #calls function to update the event

    updates_handler.update_event(update_name, event)

    logging.info("event has been added to scheduler for a news update: %s", update_name)

    return event



def store_deleted_news_article(news_article_to_store):
    '''
    function which calls other functions when a news article is deleted
    '''

    #add title to a list of deleted news article titles

    DELETED_NEWS_ARTICLES_TITLES.append(news_article_to_store)

    logging.info("News article added to list of deleted news articles: %s", news_article_to_store)

    #call function to remove news article

    remove_news_article()



def remove_news_article():
    '''
    function which removes news articles which have been deleted
    '''

    #loop through the news articles

    for article in NEWS_ARTICLES:

    #loop through the list of deleted news articles

        for title in DELETED_NEWS_ARTICLES_TITLES:

        #if a news article title is equal to a deleted news article title

            if article["title"] == title:

            #remove the news article

                NEWS_ARTICLES.remove(article)

                logging.info("News article removed from list of news articles: %s", title)
