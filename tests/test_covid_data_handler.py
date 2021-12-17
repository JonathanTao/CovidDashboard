'''
    The tasks of this file are as follows:
        - Test functions within covid_data_handler.py
'''



import time



from flaskr.covid_data_handler import parse_csv_data
from flaskr.covid_data_handler import process_covid_csv_data
from flaskr.covid_data_handler import covid_API_request
from flaskr.covid_data_handler import schedule_covid_updates
from flaskr.shared_scheduler import scheduler



def test_parse_csv_data():
    '''
    test 'parse_csv_data' function
    '''

    #call function to parse data

    data = parse_csv_data('nation_2021-10-28.csv')

    #test the length of data returned is correct

    assert len(data) == 639



def test_process_covid_csv_data():
    '''
    test 'process_covid_csv_data' function
    '''

    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))

    #test that the values for the dashboard are correct

    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544



def test_covid_API_request():
    '''
    test 'covid_API_request' function
    '''

    test_data = covid_API_request("Leicester", "ltla")

    #test that the data has been loaded in

    assert len(test_data) > 1



def test_schedule_covid_updates():
    '''
    test 'schedule_covid_updates' function
    '''

    #when testing, queue should be empty to begin with

    assert len(scheduler.queue) == 0

    #schedule an event for covid data

    schedule_covid_updates(5, "test")

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
