'''
    The tasks of this file are as follows:
        - update the covid data which is done at the start when the app is first created and when a covid data update is scheduled
        - fetches the covid data via the 'Cov19API' module   
        - parse csv data into a list  
        - processing the covid data to find the desired values                          
        - schedules covid data updates
'''



import csv
import logging
import sched
import time



from uk_covid19 import Cov19API
from flaskr import shared_config_file
from flaskr import shared_scheduler
from flaskr import updates_handler




headings = { #dictionary containing headers
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"
} 


  

data = { #dictionary containing keys for the information required to get the covid data which will be displayed on the dashboard
    "local_last7days_cases": "local_last7days_cases",
    "total_deaths": "total_deaths",
    "current_hospital_cases": "current_hospital_cases",
    "national_last7days_cases": "national_last7days_cases",
    "local_location": "local_location",
    "local_location_type": "local_location_type",
    "national_location": "national_location",
    "national_location_type": "national_location_type"
}



def get_data(title_of_update = ""): #main function which calls other functions to deal with covid data
    data["local_location"] = shared_config_file.data["covidDataDetails"]["localLocation"]     
    data["local_location_type"] = shared_config_file.data["covidDataDetails"]["localLocationType"]     
    data["national_location"] = shared_config_file.data["covidDataDetails"]["nationalLocation"]     
    data["national_location_type"] = shared_config_file.data["covidDataDetails"]["nationalLocationType"]
    
    local_csv_data = covid_API_request(data["local_location_type"], data["local_location"])
    national_csv_data = covid_API_request(data["national_location_type"], data["national_location"])
    
    data["local_last7days_cases"] = process_covid_csv_data(local_csv_data)[2]                   #get the desired values from the processing function
    data["total_deaths"], data["current_hospital_cases"], data["national_last7days_cases"] = process_covid_csv_data(national_csv_data)
    
    update = updates_handler.find_update(title_of_update)
    if update is not None: #if the update is found
        if update["repeating"]: #if the value for the key repeating is true, then schedule another update. If not then delete the update from the list of existing updates
            schedule_covid_updates(60*60*24, title_of_update)   
        else:
            updates_handler.delete_updates(title_of_update)



def covid_API_request(location_type = "ltla", location = "Exeter"): #function to get covid data
    full_location = [
        "areaType="+location_type,
        "areaName="+location
    ] 
    api = Cov19API(filters = full_location, structure = headings)  
    try:
        data = api.get_csv() #get the data
        parsed_data = parse_csv_data(data)    
        logging.info("data parsed successfully") 
    except FileNotFoundError as error: #can't find the file
        parsed_data = ""
        logging.error("csv file doesn't exist: " + error)
    return parsed_data
    
    
    
def parse_csv_data(csv_filename): #function to parse csv data into a list
    list_rows = []     
    lines = csv_filename.splitlines()        
    csvReader = csv.reader(lines)   
    list_rows = list(csvReader)       
    return list_rows     
    
    
    
def process_covid_csv_data(covid_csv_data): #gets the data and calculates the values
    try: 
        total_deaths = 0
        current_hospital_cases = 0
        last7days_cases = 0   
              
        column = find_column("cumDailyNsoDeathsByDeathDate")    
        row = first_non_empty_space(covid_csv_data, column)
        if row != -1: #if there is a non empty space
            total_deaths = int(covid_csv_data[row][column]) 
                   
        column = find_column("hospitalCases")
        row = first_non_empty_space(covid_csv_data, column)
        if row != -1: #if there is a non empty space
            current_hospital_cases = int(covid_csv_data[row][column])
        
        column = find_column("newCasesBySpecimenDate")
        row = first_non_empty_space(covid_csv_data, column) 
        if row != -1: #if there is a non empty space
            row += 1 #start counting from the row after first non empty space
            i = 0 #counter to make sure that exactly 7 rows are included
            while i < 7:
                last7days_cases += int(covid_csv_data[row][column])
                row += 1
                i += 1 
        logging.info("Covid data processed successfully")
    except:
        logging.error("Unable to process covid data")
    return total_deaths, current_hospital_cases, last7days_cases    



def schedule_covid_updates(update_interval, update_name): #schedule the event
    event = shared_scheduler.scheduler.enterabs(time.time()+update_interval, 1, get_data, (update_name,))   
    logging.info("event has been added to scheduler for a covid data update with title: " + update_name)    
    


def find_column(desired_heading): #finds column which has the heading
    i = 0
    for header in headings:        
        if desired_heading == header:
            return i
            break
        i += 1
    
    
    
def first_non_empty_space(lst, clmn): #finds first empty row within the desired column 
    i = 1 #first row is headings
    while i < len(lst):
        if lst[i][clmn] != "":
            return i
            break
        i += 1
    return -1    
    
        


    
    
    

   
    


         
     
     

        
   
        
    



        


    
    
    
