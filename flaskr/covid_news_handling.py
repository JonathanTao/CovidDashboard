'''
    The tasks of this file are as follows:
        - update the news which is done at the start when the app is first created and when a news update is scheduled        
        - fetches the news with a specified url along with parameters found in the config file
        - schedules news updates
        - stores the title of deleted news articles to make sure they are not reloaded back into the webpage when the news is updated
        - removes news articles 
'''



import requests
import json
import logging
import sched
import time



from flaskr import shared_config_file
from flaskr import shared_scheduler
from flaskr import updates_handler



news_info = {    #dictionary containing keys for the parameters required to access the news from the url
    "apiKey": "apiKey",
    "from": "from",
    "language": "language",    
    "pageSize": "pageSize", 
    "sortBy": "sortBy",
    "terms": "terms"
}



news_articles = [] #list of news articles
deleted_news_articles_titles = [] #list of the titles of deleted news articles



def update_news(title_of_update = ""): #function which calls other functions in order to update the news. This includes getting the news from the url as well as removing news articles which were desired by the user
    global news_articles
 
    news_info["apiKey"] = shared_config_file.data["newsDetails"]["apiKey"]
    news_info["from"] = shared_config_file.data["newsDetails"]["from"]
    news_info["language"] = shared_config_file.data["newsDetails"]["language"]
    news_info["pageSize"] = shared_config_file.data["newsDetails"]["pageSize"]
    news_info["sortBy"] = shared_config_file.data["newsDetails"]["sortBy"]
    news_info["terms"] = shared_config_file.data["newsDetails"]["covidTerms"]
    
    news_articles = news_API_request(news_info["terms"])
    remove_news_article()   
        
    update = updates_handler.find_update(title_of_update)
    if update is not None: #if the update is found
        if update["repeating"]: #if the value for the key repeating is true, then schedule another update. If not then delete the update from the list of existing updates
            schedule_news_updates(60*60*24, title_of_update)   
        else:
            updates_handler.delete_updates(title_of_update)   
    
     
     


    

def news_API_request(covid_terms = "Covid COVID-19 coronavirus"): #function to get news articles from website    
    terms_to_search = ""
   
    for element in list(map(str, covid_terms.split())): #split into a new item in the list everytime a space is seen. Then loop through each element in list
        if terms_to_search == "": #if the element is the first element, no need to add ' OR '
            terms_to_search += element #just add element to list
        else:
            terms_to_search += " OR " + element #add ' OR ' followed by element
    
    parameters = {            
        "apiKey": news_info["apiKey"],
        "from": news_info["from"],
        "language": news_info["language"],
        "pageSize": news_info["pageSize"],
        "sortBy": news_info["sortBy"],
        "q": terms_to_search        
    }    
     
    url = shared_config_file.data["newsDetails"]["apiUrl"]
    try: 
        data = requests.get(url, params = parameters) #assign return value from a get request to the corresponding url with the corresponding parameters
        news = json.loads(data.text)["articles"] #assign the value associated to the "articles" key to be the news        
        logging.info("News fetched successfully")
    except requests.exceptions.ConnectionError as error: #cannot connect to the server        
        logging.error("Unable to fetch news articles: " + str(error))        
    return news    
    
    
    
def schedule_news_updates(update_interval, update_name): #schedule the event
    event = shared_scheduler.scheduler.enterabs(time.time()+update_interval, 1, update_news, (update_name,)) 
    logging.info("event has been added to scheduler for a news update with title: " + update_name)    
    
    
    
def store_deleted_news_article(news_article_to_store): #function which calls other functions when a news article is deleted
    global deleted_news_articles_titles    
    
    deleted_news_articles_titles.append(news_article_to_store)
    logging.info("News article added to list of deleted news articles: " + news_article_to_store) #add to a list of deleted news articles
    remove_news_article()    



def remove_news_article(): #function which removes news articles
    global deleted_news_articles_titles            
    global news_articles

    for article in news_articles: #loop through the news articles
        for title in deleted_news_articles_titles: #loop through the list of deleted news articles
            if article["title"] == title: #if a news article title is equal to a deleted news article title, remove the news article
                news_articles.remove(article)
                logging.info("News article removed from list of news articles: " + title)
    
    



    

                                             

