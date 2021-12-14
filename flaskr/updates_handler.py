'''
    The tasks of this file are as follows:
        - schedules covid data and news updates when an update is first submitted
        - finds the update that the user is looking for
        - deletes updates from the list of alarmed updates
        - cancels updates from the scheduler's queue
        - adds updates to the list of alarmed updates        
'''



import logging



from datetime import datetime
from flaskr import covid_data_handler
from flaskr import covid_news_handling
from flaskr import shared_scheduler



counter = 0 #used to give each update a unique title so it can be distinguished by concatenating itself with the update label
alarmed_updates = [] #list of updates



def schedule_updates(name, time_interval, repeat, covid_data, covid_news): #used to schedule an update when the submit button is clicked
    global alarmed_updates
    global counter
    
    counter += 1 #add 1 each time so that each update has a unique title
    
    repeating = get_values_for_content(repeat)
    display_covid_data = get_values_for_content(covid_data) #call functions to get corresponding true or false values
    display_news = get_values_for_content(covid_news)

    title = "Update" +  str(counter) + " " + name
    
    try:
        current_date = datetime.now()  #get current time
        current_date_string = datetime.strftime(current_date, "%H:%M") #turn that into a string displaying only hours and minutes
        current_time = datetime.strptime(current_date_string, "%H:%M") #then turn it into a datetime object with only hours and minutes
        update_time = datetime.strptime(time_interval, "%H:%M") #get the time put in the time section and turn it from a string into a datetime object with only hours and minutes
        difference = update_time - current_time #find the difference in time
        seconds_until_update = difference.total_seconds() #convert to seconds               
        if display_covid_data: #if this is true then schedule an event for covid data
            covid_data_handler.schedule_covid_updates(seconds_until_update, title)
        if display_news: #if this is true then schedule an event for covid news
            covid_news_handling.schedule_news_updates(seconds_until_update, title)
        add_updates(title, time_interval, repeating, display_covid_data, display_news)
    except: #will occur if a time is not given. In this case an event will still appear as a tab but with no time
        logging.warning("event has not been given a time: " + title)
        add_updates(title, None, repeating, display_covid_data, display_news)
        


def find_update(title): #used to find the update by its unique title
    global alarmed_updates
    
    for update in alarmed_updates: #loop through all updates
        if title == update["title"]:
            return update
    return None           
           
           
        
def delete_updates(title): #used to delete update through its unique title
    global alarmed_updates
        
    for update in alarmed_updates: #loop through all updates
        if title == update["title"]: 
            alarmed_updates.remove(update)
            logging.info("Update has been removed from list: " + title)



def cancel_updates(title): #used to cancel an update/event through its unique title
    global alarmed_updates
    
    for update in alarmed_updates: #loop through all updates
        if title == update["title"]:
            shared_scheduler.scheduler.cancel(update["event"])
            logging.info("Event has been cancelled: " + title)
    
    
    
def add_updates(title, time_interval, repeating, display_covid_data, display_news): #used to add an update to a list of updates which will then be displayed on the page
    global alarmed_updates   
    
    if time_interval is not None: #if a time was not given
        time_for_update = time_interval
    else:
        time_for_update = "No time input"
        
    alarmed_updates.append({"title" : title, #appends a dictionary to the list of updates
                            "content" : "Time of update: " + time_for_update 
                            + ". Repeating: " + str(repeating) 
                            + ". Display covid data: " + str(display_covid_data) 
                            + ". Display news: " + str(display_news),
                            "repeating" : repeating})   
    logging.info("Update has been added to list: " + title)
    
        
    
def get_values_for_content(variable): #used to get corresponding true or false values
    if variable is None:
        return False
    else:
        return True