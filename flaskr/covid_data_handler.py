'''
    The tasks of this file are as follows:
        - update the covid data
        - fetches the covid data via the 'Cov19API' module
        - parse csv data into a list
        - processing the covid data to find the desired values
        - schedules covid data updates
'''



import csv
import logging
import time



from uk_covid19 import Cov19API
from flaskr import shared_config_file
from flaskr import shared_scheduler
from flaskr import updates_handler



#dictionary containing headers

headings = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"
}



#dictionary containing keys for the information required to get the covid data

data = {
    "localLast7daysCases": "localLast7daysCases",
    "totalDeaths": "totalDeaths",
    "currentHospitalCases": "currentHospitalCases",
    "nationalLast7daysCases": "nationalLast7daysCases",
    "localLocation": "localLocation",
    "localLocationType": "localLocationType",
    "nationalLocation": "nationalLocation",
    "nationalLocationType": "nationalLocationType"
}



def get_data(title_of_update = ""):
    '''
    function which calls other functions to deal with covid data
    '''

    data["localLocation"] = shared_config_file.data["covidData"]["localLocation"]
    data["localLocationType"] = shared_config_file.data["covidData"]["localLocationType"]
    data["nationalLocation"] = shared_config_file.data["covidData"]["nationalLocation"]
    data["nationalLocationType"] = shared_config_file.data["covidData"]["nationalLocationType"]

    local_csv_data = covid_API_request(data["localLocationType"], data["localLocation"])
    national_csv_data = covid_API_request(data["nationalLocationType"], data["nationalLocation"])

    local_last7days_cases = process_covid_csv_data(local_csv_data)[2]
    deaths, hospital_cases, national_last7days_cases = process_covid_csv_data(national_csv_data)

    data["localLast7daysCases"] = local_last7days_cases
    data["totalDeaths"] = deaths
    data["currentHospitalCases"] = hospital_cases
    data["nationalLast7daysCases"] = national_last7days_cases

    #call function to find update

    update = updates_handler.find_update(title_of_update)

    #if the update is found

    if update is not None:

    #if the value for this key is true, then schedule another update

        if update["repeating"]:

            schedule_covid_updates(60*60*24, title_of_update)

    #if not then delete the update from the list of existing updates

        else:

            updates_handler.delete_updates(title_of_update)



def covid_API_request(location_type = "ltla", location = "Exeter"):
    '''
    function to get covid data
    '''

    #specifies full location to get data

    full_location = [
        "areaType="+location_type,
        "areaName="+location
    ]

    #sets details to get data

    api = Cov19API(filters = full_location, structure = headings)

    try:

        #get the data

        csv_data = api.get_csv()

        #call function to parse data

        parsed_data = parse_csv_data(csv_data)

        logging.info("data parsed successfully")

    except FileNotFoundError as error:

        #can't find the file

        parsed_data = ""

        logging.error("csv file doesn't exist: %s", error)

    return parsed_data



def parse_csv_data(csv_filename):
    '''
    function to parse csv data into a list
    '''

    list_rows = []

    #splits csv file into lines

    lines = csv_filename.splitlines()

    #reads the csv data

    csv_reader = csv.reader(lines)

    #converts from csv format to list

    list_rows = list(csv_reader)

    return list_rows



def process_covid_csv_data(covid_csv_data):
    '''
    gets the data and calculates the values
    '''

    try:
        total_deaths = 0
        current_hospital_cases = 0
        last7days_cases = 0

        #call function to find column

        column = find_column("cumDailyNsoDeathsByDeathDate")

        #call function to find row to start on

        row = first_non_empty_space(covid_csv_data, column)

        #if there is a non empty space and column is found

        if row != -1 and column != -1:
            total_deaths = int(covid_csv_data[row][column])

        #call function to find column

        column = find_column("hospitalCases")

        #call function to find row to start on

        row = first_non_empty_space(covid_csv_data, column)

        #if there is a non empty space and column is found

        if row != -1 and column != -1:
            current_hospital_cases = int(covid_csv_data[row][column])

        #call function to find column

        column = find_column("newCasesBySpecimenDate")

        #call function to find row to start on

        row = first_non_empty_space(covid_csv_data, column)

        #if there is a non empty space and column is found

        if row != -1 and column != -1:

            #start counting from the row after first non empty space

            row += 1

            #counter to make sure that exactly 7 rows are included

            i = 0

            #while 7 rows have not been counted

            while i < 7:

                last7days_cases += int(covid_csv_data[row][column])

                row += 1

                i += 1

        logging.info("Covid data processed successfully")

    #unable to find data to process

    except FileNotFoundError as error:

        logging.error("Cannot find data to process: %s", error)

    return total_deaths, current_hospital_cases, last7days_cases



def schedule_covid_updates(update_interval, update_name):
    '''
    schedule the update
    '''

    event = shared_scheduler.scheduler.enterabs(
        time.time()+update_interval, 1, get_data, (update_name,))

    #calls function to update the event

    updates_handler.update_event(update_name, event)

    logging.info("event has been added to scheduler for a covid data update: %s", update_name)

    return event




def find_column(desired_heading):
    '''
    finds column which has the heading
    '''

    i = 0

    #loop through the 'headings' dictionary

    for header in headings:

        #if the header needed is found in the 'headings' dictionary

        if desired_heading == header:

            return i

        i += 1

    #no heading found

    return -1



def first_non_empty_space(lst, clmn):
    '''
    finds first empty row within the desired column
    '''

    #first row is headings

    i = 1

    #while not past the end of the data

    while i < len(lst):

        #if the cell is not blank

        if lst[i][clmn] != "":

            return i

        i += 1

    #no non empty space

    return -1
