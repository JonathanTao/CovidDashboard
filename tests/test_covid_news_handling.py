'''
    The tasks of this file are as follows:
        - Test functions within covid_news_handling.py
'''


from flaskr.covid_news_handling import news_API_request
from flaskr.covid_news_handling import schedule_news_updates
from flaskr.covid_news_handling import store_deleted_news_article
from flaskr.covid_news_handling import remove_news_article
from flaskr.covid_news_handling import news_articles
from flaskr.covid_news_handling import deleted_news_articles_titles
from flaskr.shared_scheduler import scheduler



def test_news_API_request():
    test_data = news_API_request("Covid COVID-19 coronavirus")    
    assert len(test_data) > 1 #test that news articles have been loaded in
    
    
    
def test_schedule_news_updates():    
    assert len(scheduler.queue) == 0 #when testing, queue should be empty to begin with
    
    schedule_news_updates(5, "test")   
    
    assert len(scheduler.queue) == 1 #test that update has been added to queue    
    
    scheduler.run(blocking = False)
    
    assert len(scheduler.queue) == 1 #test that the update is still in the queue after scheduler.run has been called
    
    time.sleep(5) #wait 5 seconds
    
    scheduler.run(blocking = False)
    
    assert len(scheduler.queue) == 0 #test that the update is no longer in the queue
    
    
    
def test_store_deleted_news_article():  
    assert len(deleted_news_articles_titles) == 0 #when testing, list should be empty to begin with

    test_title = "hello world"
    
    store_deleted_news_article(test_title)
    
    assert len(deleted_news_articles_titles) == 1 #test the news article title has been added to the list
    
    

def test_remove_news_article():
    assert len(news_articles) == 0 #when testing, list should be empty to begin with
    
    news_articles.append({"title": "test", "content" : "hello world"}) #add test news article to list of news articles
    
    assert len(news_articles) == 1 #test the news article has been added to the list
    
    store_deleted_news_article("test") #add news article title to list of deleted news article titles
    
    remove_news_article()
    
    assert len(news_articles) == 0 #test that the news article is no longer in the list
    
