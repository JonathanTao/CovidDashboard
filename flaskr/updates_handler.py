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



#used to give each update a unique title

COUNTER = 0

#list of updates

ALARMED_UPDATES = []



def schedule_updates(name, time_interval, repeat, covid_data, covid_news):
    '''
    used to schedule an update when the submit button is clicked
    '''

    global COUNTER

    #add 1 each time so that each update has a unique title

    COUNTER += 1

    title = "Update" +  str(COUNTER) + " " + name

    try:

    #get current time

        current_date = datetime.now()

        #turn that into a string displaying in hours and minutes

        current_date_string = datetime.strftime(current_date, "%H:%M")

        #then turn it into a datetime object in hours and minutes

        current_time = datetime.strptime(current_date_string, "%H:%M")

        #get the update time and turn it from a string into a datetime object in hours and minutes

        update_time = datetime.strptime(time_interval, "%H:%M")

        #find the difference in time

        difference = update_time - current_time

        #convert to seconds

        seconds_until_update = difference.total_seconds()

        #if this is true then schedule an event for covid data

        if covid_data is not None:

            event = covid_data_handler.schedule_covid_updates(seconds_until_update, title)

            #call function to add the update to list of updates

            add_updates(title, time_interval, repeat, covid_data, covid_news)

            #calls function to update the event

            update_event(title, event)

        #if this is true then schedule an event for covid news

        if covid_news is not None:

            event = covid_news_handling.schedule_news_updates(seconds_until_update, title)

            #call function to add the update to list of updates

            add_updates(title, time_interval, repeat, covid_data, covid_news)

            #calls function to update the event

            update_event(title, event)

    #will occur if a time is not given
    #in this case an event will still appear as a tab but with no time

    except ValueError as error:

        logging.warning("event has not been given a time: %s", error)

        #call function to add the update to list of updates

        add_updates(title, None, repeat, covid_data, covid_news)



def find_update(title):
    '''
    used to find the update by its unique title
    '''

    #loop through all updates

    for update in ALARMED_UPDATES:

    #if the title passed through is equal to one of the titles of the updates in alarmed updates

        if title == update["title"]:

            return update

    return None



def delete_updates(title):
    '''
    used to delete update through its unique title
    '''

    #loop through all updates

    for update in ALARMED_UPDATES:

    #if the title passed through is equal to one of the titles of the updates in the list of updates

        if title == update["title"]:

        #remove the update from list of updates

            ALARMED_UPDATES.remove(update)

            logging.info("Update has been removed from list: %s", title)



def cancel_event(title):
    '''
    used to cancel an event through its unique title
    '''

    #loop through all updates

    for update in ALARMED_UPDATES:

    #if the title passed through is equal to one of the titles of the updates in the list of updates

        if title == update["title"]:

        #if an update exists, cancel the update

            if update["event"] is not None:

                shared_scheduler.scheduler.cancel(update["event"])

                logging.info("Event has been cancelled: %s", title)

            else:

                logging.info("Not time on the update so no event cancelled: %s", title)



def add_updates(title, time_interval, repeat, covid_data, covid_news):
    '''
    used to add an update to a list of updates which will then be displayed on the page
    '''

    #call functions to get corresponding true or false values

    repeating = get_values_for_content(repeat)
    display_covid_data = get_values_for_content(covid_data)
    display_news = get_values_for_content(covid_news)

    #if a time was given

    if time_interval is not None:

        time_for_update = time_interval

    #if a time was not given

    else:

        time_for_update = "No time input"

    #appends a dictionary to the list of updates
    #key 'event' has value 'None' and will changed later by the function 'update_event'

    ALARMED_UPDATES.append({"title" : title,
                            "content" : "Time of update: " + time_for_update
                            + ". Repeating: " + str(repeating)
                            + ". Display covid data: " + str(display_covid_data)
                            + ". Display news: " + str(display_news),
                            "repeating" : repeating,
                            "event" : None})

    logging.info("Update has been added to list: %s", title)



def update_event(title, event):
    '''
    used to update an event through its unique title
    '''

    #loop through all updates

    for update in ALARMED_UPDATES:

    #if the title passed through is equal to one of the titles of the updates in the list of updates

        if title == update["title"]:

            #update the 'event' key for that particular update

            update["event"] = event

            logging.info("Event has been updated: %s", title)



def get_values_for_content(variable):
    '''
    used to get corresponding true or false values
    '''

    if variable is None:

        return False

    return True
