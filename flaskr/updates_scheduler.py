import logging

from datetime import datetime
from flaskr import covid_data_handler
from flaskr import covid_news_handling
from flaskr import shared_scheduler

counter = 0

alarmed_updates = []

def schedule_updates(name, time_interval, repeat, covid_data, covid_news):
    global alarmed_updates
    global counter
    
    counter = counter + 1
    
    repeating = get_values_for_content(repeat)
    display_covid_data = get_values_for_content(covid_data)
    display_news = get_values_for_content(covid_news)

    just_scheduled = True
    
    title = "Update" +  str(counter) + " " + name
    
    event = None
    
    try:
        current_date = datetime.now()  
        current_date_string = datetime.strftime(current_date, "%H:%M")
        current_time = datetime.strptime(current_date_string, "%H:%M")
        update_time = datetime.strptime(time_interval, "%H:%M")
        difference = update_time - current_time
        seconds_until_update = difference.total_seconds()                   
        if covid_data != None:  
            event = shared_scheduler.scheduler.enterabs(time.time()+seconds_until_update, 1, covid_data_handler.get_data, (title, time_interval, repeating, display_covid_data, display_news, False, just_scheduled))  
            logging.info("event has been added to scheduler with title: " + title)
        if covid_news != None:
            event = shared_scheduler.scheduler.enterabs(time.time()+seconds_until_update, 1, covid_news_handling.update_news, (title, time_interval, repeating, display_covid_data, display_news, False, just_scheduled))    
            logging.info("event has been added to scheduler with title: " + title)
        add_updates(event, title, time_interval, repeating, display_covid_data, display_news)
    except:
        logging.warning("event has not been given a time: " + title)
        add_updates(None, title, None, repeating, display_covid_data, display_news)
        
        
        
def delete_updates(title):
    global alarmed_updates
        
    for update in alarmed_updates:
        if title == update["title"]:
            alarmed_updates.remove(update)
            logging.info("Update has been removed from list: " + title)



def cancel_updates(title):
    global alarmed_updates
    
    for update in alarmed_updates:
        if title == update["title"]:
            shared_scheduler.scheduler.cancel(update["event"])
            logging.info("Event has been cancelled: " + title)
    
    
    
def add_updates(event, title, time_interval, repeating, display_covid_data, display_news):
    global alarmed_updates   
    
    if time_interval != None:
        time_for_update = time_interval
    else:
        time_for_update = "No time input"
        
    alarmed_updates.append({"event" : event,
                            "title" : title,
                            "content" : "Time of update: " + time_for_update + ". Repeating: " + str(repeating) + ". Display covid data: " + str(display_covid_data) + ". Display news: " + str(display_news)})
    logging.info("Update has been added to list: " + title)
    
        
    
def get_values_for_content(variable):
    if variable == None:
        return False
    else:
        return True