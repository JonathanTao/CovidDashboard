'''
    __init__.py requires python to treat this directory as a package
    The tasks of this file are as follows:
        - creating and configuring the main flask application        
        - getting the covid data and news articles for when the application has just been created
        - setting up the logging details based on the information given by the config file
        - binds the url '/index' to the index function    
        - displays the index.html webpage with the covid data, news articles and updates by rendering them into the webpage
        - handles GET requests that occur within the URL
        - runs the scheduler
'''



import logging
import os



from flask import Flask
from flask import render_template
from flask import request



from flaskr import covid_data_handler
from flaskr import covid_news_handling
from flaskr import shared_config_file
from flaskr import shared_scheduler
from flaskr import updates_handler



def create_app(test_config=None):   
    app = Flask(__name__, instance_relative_config=True) #creates and configures the app   
        
    logging.basicConfig(filename = shared_config_file.data["loggingDetails"]["file"], #setting up logging details
                        format = shared_config_file.data["loggingDetails"]["format"],
                        level = shared_config_file.data["loggingDetails"]["level"],
                        force = True)
                        
    logging.info("app started")
    
    covid_data_handler.get_data()    
    covid_news_handling.update_news()    
                
    @app.route("/index")           
    def index():    
        dashboard_title = shared_config_file.data["covidDataDetails"]["title"]
        favicon = shared_config_file.data["covidDataDetails"]["favicon"]
                      
        scheduled_update_title = request.args.get("alarm_item") #get the argument returned from update tabs      
        if scheduled_update_title != None: #if the argument returned has a value
            logging.info("GET request on 'alarm_item'")
            updates_handler.delete_updates(scheduled_update_title)
            updates_handler.cancel_updates(scheduled_update_title)
    
        news_title = request.args.get("notif") #get the argument returned from news tabs    
        if news_title != None: #if the argument returned has a value
            logging.info("GET request on 'notif'")
            covid_news_handling.store_deleted_news_article(news_title)       
        
        update_name = request.args.get("two") #get the argument returned from update label
        if update_name != None: #if the argument returned has a value, this means that the submit button was clicked as the update label required when setting up an update
            logging.info("GET request on 'two'")
            update_time = request.args.get("alarm") #get the argument returned from the time section
            repeat_update = request.args.get("repeat") #get the argument returned from the repeat checkbox
            update_covid_data = request.args.get("covid-data") #get the argument returned from the covid data checkbox
            update_covid_news = request.args.get("news") #get the argument returned from the news checkbox
            updates_handler.schedule_updates(update_name, update_time, repeat_update, update_covid_data, update_covid_news)        
        
        articles = covid_news_handling.news_articles          
        scheduled_updates = updates_handler.alarmed_updates
        
        logging.debug("scheduler queue before scheduler run: " + str(shared_scheduler.scheduler.queue))
        
        logging.info("scheduler running events")
        shared_scheduler.scheduler.run(blocking = False) #run the scheduler which will run the updates in the scheduler queue when the time is reached
        
        logging.debug("scheduler queue after scheduler run: " + str(shared_scheduler.scheduler.queue))
                                
        return render_template("index.html", #render the webpage with the info
            title = dashboard_title,
            location = covid_data_handler.data["local_location"],
            local_7day_infections = covid_data_handler.data["local_last7days_cases"],
            nation_location = covid_data_handler.data["national_location"],
            national_7day_infections = covid_data_handler.data["national_last7days_cases"],
            hospital_cases = covid_data_handler.data["current_hospital_cases"],
            deaths_total = covid_data_handler.data["total_deaths"],
            news_articles = articles,
            updates = scheduled_updates,
            image = favicon)

    return app