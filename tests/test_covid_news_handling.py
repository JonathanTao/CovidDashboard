'''
    The tasks of this file are as follows:
        - Test functions within covid_news_handling.py
'''



import time



from flaskr.covid_news_handling import news_API_request
from flaskr.covid_news_handling import schedule_news_updates
from flaskr.covid_news_handling import store_deleted_news_article
from flaskr.covid_news_handling import remove_news_article
from flaskr.covid_news_handling import NEWS_ARTICLES
from flaskr.covid_news_handling import DELETED_NEWS_ARTICLES_TITLES
from flaskr.shared_scheduler import scheduler



def test_news_API_request():
    '''
    test 'news_API_request' function
    '''

    #call function to get news

    test_data = news_API_request("Covid COVID-19 coronavirus")

    #test that news articles have been loaded in

    assert len(test_data) > 1



def test_schedule_news_updates():
    '''
    test 'schedule_news_updates' function
    '''

    #when testing, queue should be empty to begin with

    assert len(scheduler.queue) == 0

    #call function to get news

    schedule_news_updates(5, "test")

    #test that update has been added to queue

    assert len(scheduler.queue) == 1

    #run the scheduler

    scheduler.run(blocking = False)

    #test that the update is still in the queue after scheduler.run has been called

    assert len(scheduler.queue) == 1

    #wait 5 seconds

    time.sleep(5)

    #run the scheduler

    scheduler.run(blocking = False)

    #test that the update is no longer in the queue

    assert len(scheduler.queue) == 0



def test_store_deleted_news_article():
    '''
    test 'store_deleted_news_article' function
    '''

    #when testing, list should be empty to begin with

    assert len(DELETED_NEWS_ARTICLES_TITLES) == 0

    test_title = "hello world"

    #call function to deal with deleted news article

    store_deleted_news_article(test_title)

    #test the news article title has been added to the list

    assert len(DELETED_NEWS_ARTICLES_TITLES) == 1



def test_remove_news_article():
    '''
    test 'test_remove_news_article' function
    '''

    #when testing, list should be empty to begin with

    assert len(NEWS_ARTICLES) == 0

    #add test news article to list of news articles

    NEWS_ARTICLES.append({"title": "test", "content" : "hello world"})

    #test the news article has been added to the list

    assert len(NEWS_ARTICLES) == 1

    #add news article title to list of deleted news article titles

    store_deleted_news_article("test")

    #call function to remove news article

    remove_news_article()

    #test that the news article is no longer in the list

    assert len(NEWS_ARTICLES) == 0
