'''
    The tasks of this file are as follows:
        - Test functions within updates_handler.py
'''



from flaskr.updates_handler import add_updates
from flaskr.updates_handler import find_update
from flaskr.updates_handler import delete_updates
from flaskr.updates_handler import cancel_event
from flaskr.updates_handler import update_event
from flaskr.updates_handler import ALARMED_UPDATES
from flaskr.covid_data_handler import schedule_covid_updates
from flaskr.covid_news_handling import schedule_news_updates
from flaskr.shared_scheduler import scheduler



def test_add_updates():
    '''
    test 'add_updates' function
    '''

    #when testing, list should be empty to begin with

    assert len(ALARMED_UPDATES) == 0

    #when a time is given

    add_updates("test", "14:00", False, True, False)

    #test the update has been added to the list

    assert len(ALARMED_UPDATES) == 1

    #when a time is not given

    add_updates("test", None, False, True, False)

    #test the update has been added to the list

    assert len(ALARMED_UPDATES) == 2



def test_find_update():
    '''
    test 'find_update' function
    '''

    #call function to add an update

    add_updates("test", None, False, True, False)

    #call function to find update

    update = find_update("test")

    #test that update should be found

    assert update is not None

    #call function to find update

    update = find_update("hello")

    #test that update should not be found

    assert update is None



def test_delete_updates():
    '''
    test 'delete_updates' function
    '''

    #when testing, list should be empty to begin with

    assert len(ALARMED_UPDATES) == 0

    #call function to add an update

    add_updates("test", "14:00", False, True, False)

    #test the update has been added to the list

    assert len(ALARMED_UPDATES) == 1

    #call function to delete an update

    delete_updates("test")

    #test the update has been removed from the list

    assert len(ALARMED_UPDATES) == 0



def test_cancel_event():
    '''
    test 'cancel_event' function
    '''

    #when testing, queue should be empty to begin with

    assert len(scheduler.queue) == 0

    #schedule a covid update

    event = schedule_covid_updates(5, "hello")

    #test the update has been added to the queue

    assert len(scheduler.queue) == 1

    #cancel the event

    cancel_event("hello")

    #test that the update has been removed from the queue

    assert len(scheduler.queue) == 0

    #schedule a news update

    event = schedule_news_updates(5, "hello")

    #test the update has been added to the queue

    assert len(scheduler.queue) == 1

    #cancel the event

    cancel_event("hello")

    #test that the update has been removed from the queue

    assert len(scheduler.queue) == 0
