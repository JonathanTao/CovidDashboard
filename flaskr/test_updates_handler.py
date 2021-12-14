'''
    The tasks of this file are as follows:
        - Test functions within updates_handler.py
'''



from flaskr.updates_handler import add_updates
from flaskr.updates_handler import find_update
from flaskr.updates_handler import delete_updates
from flaskr.updates_handler import cancel_updates
from flaskr.updates_handler import alarmed_updates
from flaskr.covid_data_handler import schedule_covid_updates
from flaskr.covid_news_handling import schedule_news_updates



def test_add_updates():
    assert len(alarmed_updates) == 0 #when testing, list should be empty to begin with
    
    add_updates("test", "14:00", False, True, False) #when a time is given
    
    assert len(alarmed_updates) == 1 #test the update has been added to the list
    
    add_updates("test", None, False, True, False) #when a time is not given
    
    assert len(alarmed_updates) == 2 #test the update has been added to the list
    


def test_find_update():
    add_updates("test", None, False, True, False) #add an update
    
    update = find_update("test")
    
    assert update != None #test that update should be found
    
    update = find_update("hello")
    
    assert update == None #test that update should not be found
    
    
    
def test_delete_updates():
    assert len(alarmed_updates) == 0 #when testing, list should be empty to begin with

    add_updates("test", "14:00", False, True, False) #add an update
    
    assert len(alarmed_updates) == 1 #test the update has been added to the list
    
    delete_updates("test") 
    
    assert len(alarmed_updates) == 0 #test the update has been removed from the list
    
    

def test_cancel_updates():
    assert len(shared_scheduler.scheduler.queue) == 0 #when testing, queue should be empty to begin with

    schedule_covid_updates(5, "hello") #schedule a covid update
    
    assert len(shared_scheduler.scheduler.queue) == 1 #test the update has been added to the queue
    
    cancel_updates("hello")
    
    assert len(shared_scheduler.scheduler.queue) == 0 #test that the update has been removed from the queue
    
    schedule_news_updates(5, "hello") #schedule a covid update
    
    assert len(shared_scheduler.scheduler.queue) == 1 #test the update has been added to the queue
    
    cancel_updates("hello")
    
    assert len(shared_scheduler.scheduler.queue) == 0 #test that the update has been removed from the queue
    
    
    
    