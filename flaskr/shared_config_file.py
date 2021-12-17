'''
    The tasks of this file are as follows:
        - Attempt to open the users config file and provides default if unable to
'''



import json
import logging



#dictionary which stores all the data and information from the configuration file

data = {}



#the default configuration file if none is provided by the user

default = {
	"covidData": {
		"favicon" : "favicon.ico",
		"localLocation": "Exeter",
		"localLocationType": "ltla",
		"nationalLocation": "England",
		"nationalLocationType": "nation",
		"title" : "COVID-19 Data"
	},
	"logging": {
		"file" : "flaskr/logs/logs.log",
		"format" : "%(levelname)s:%(name)s: [%(asctime)s] - %(message)s",
        "level" : 10
	},
	"news": {
		"apiKey": "c48d6a7b8d91457ca376559311285019",
		"apiUrl" : "https://newsapi.org/v2/everything",
		"covidTerms": "Covid COVID-19 coronavirus",
		"from" : 3,
        "language" : "en",
		"pageSize": 5,
        "sortBy" : "publishedAt"
	}
}



#try to open the config file which should be provided by the user

try:
    with open("flaskr/config.json", encoding="utf-8") as jsonfile:

        #load in file as json format

        data = json.load(jsonfile)

    logging.info("config file successfully opened")

#if the file cannot be found then use the default config file

except FileNotFoundError:

    logging.warning("config file doesn't exist")

    #set config file to default

    data = default

    logging.info("default config file will be used")
