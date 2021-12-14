'''
    The tasks of this file are as follows:
        - Attempt to open the users config file and if this doesn't succeed then provide them with the default config file
'''



import json
import logging



data = {} #dictionary which stores all the data and information from the configuration file



default = { #the default configuration file if none is provided by the user
	"covidDataDetails": {
		"favicon" : "favicon.ico",
		"localLocation": "Exeter",
		"localLocationType": "ltla",
		"nationalLocation": "England",
		"nationalLocationType": "nation",
		"title" : "COVID-19 Data"
	},
	"loggingDetails": {
		"file" : "flaskr/logs/logs.log",
		"format" : "%(levelname)s:%(name)s: [%(asctime)s] - %(message)s",		
        "level" : 10
	},
	"newsDetails": {		
		"apiKey": "c48d6a7b8d91457ca376559311285019",		
		"apiUrl" : "https://newsapi.org/v2/everything",
		"covidTerms": "Covid COVID-19 coronavirus",
		"from" : 3,
        "language" : "en",	
		"pageSize": 5,		
        "sortBy" : "publishedAt"	
	}
}



try: #try to open the config file which should be provided by the user
    with open("flaskr/config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    logging.info("config file successfully opened")
except FileNotFoundError: #if the file cannot be found then use the default config file
    logging.warning("config file doesn't exist")
    data = default
    logging.info("default config file will be used")


