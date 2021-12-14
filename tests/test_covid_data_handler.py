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
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639 #test the length of data returned is correct
    
    

def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240_299 
    assert current_hospital_cases == 7_019 #test that the correct values for the dashboard are correct
    assert total_deaths == 141_544
    


def test_covid_API_request():
    test_data = covid_API_request("Leicester", "ltla")    
    assert len(test_data) > 1 #test that the data has been loaded in
    
    
    
def test_schedule_covid_updates():    
    assert len(scheduler.queue) == 0 #when testing, queue should be empty to begin with
    
    schedule_covid_updates(5, "test")   
    
    assert len(scheduler.queue) == 1 #test that update has been added to queue
    
    scheduler.run(blocking = False)
    
    assert len(scheduler.queue) == 1 #test that the update is still in the queue after scheduler.run has been called
    
    time.sleep(5) #wait 5 seconds
    
    scheduler.run(blocking = False)
    
    assert len(scheduler.queue) == 0 #test that the update is no longer in the queue
    
    