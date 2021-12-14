import json
import logging

default = {
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