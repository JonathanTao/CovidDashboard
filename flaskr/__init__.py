'''
    __init__.py requires python to treat this directory as a package
    The tasks of this file are as follows:
        - creating and configuring the main flask application
        - getting the covid data and news articles for when the application has just been created
        - setting up the logging details based on the information given by the config file
        - binds the url '/index' to the index function
        - displays the index.html webpage with the covid data, news articles and updates
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



def create_app():

    '''
    creates and configures the app
    '''

    app = Flask(__name__, instance_relative_config=True)

    #setting up logging details

    logging.basicConfig(filename = shared_config_file.data["logging"]["file"],
                        format = shared_config_file.data["logging"]["format"],
                        level = shared_config_file.data["logging"]["level"],
                        force = True)

    logging.info("app started")

    #call function to get covid data

    covid_data_handler.get_data()

    #call function to get news

    covid_news_handling.update_news()

    #binds the url '/index' to the index function

    @app.route("/index")

    def index():

        dashboard_title = shared_config_file.data["covidData"]["title"]
        favicon = shared_config_file.data["covidData"]["favicon"]

        #get the argument returned from update tabs

        scheduled_update_title = request.args.get("alarm_item")

        #if the argument returned has a value

        if scheduled_update_title is not None:

            logging.info("GET request on 'alarm_item'")

            #call function to delete update

            updates_handler.delete_updates(scheduled_update_title)

            #call function to cancel update

            updates_handler.cancel_event(scheduled_update_title)

        #get the argument returned from news tabs

        news_title = request.args.get("notif")

        #if the argument returned has a value

        if news_title is not None:

            logging.info("GET request on 'notif'")

            #call function to deal with deleted news article

            covid_news_handling.store_deleted_news_article(news_title)

        #get the argument returned from update label

        name = request.args.get("two")

        #if the argument returned has a value, this means that the submit button was clicked
        #this is due to the update label being compulsory

        if name is not None:

            logging.info("GET request on 'two'")

            #get the argument returned from the time section

            time = request.args.get("alarm")

            #get the argument returned from the repeat checkbox

            update = request.args.get("repeat")

            #get the argument returned from the covid data checkbox

            covid_data = request.args.get("covid-data")

            #get the argument returned from the news checkbox

            covid_news = request.args.get("news")

            #call function which prepares to schedule update

            updates_handler.schedule_updates(name, time, update, covid_data, covid_news)

        articles = covid_news_handling.NEWS_ARTICLES
        scheduled_updates = updates_handler.ALARMED_UPDATES

        logging.debug("scheduler queue before scheduler run: %s", shared_scheduler.scheduler.queue)

        logging.info("scheduler running events")

        #run the scheduler

        shared_scheduler.scheduler.run(blocking = False)

        logging.debug("scheduler queue after scheduler run: %s", shared_scheduler.scheduler.queue)

        #render the webpage with the info

        return render_template("index.html",
            title = dashboard_title,
            location = covid_data_handler.data["localLocation"],
            local_7day_infections = covid_data_handler.data["localLast7daysCases"],
            nation_location = covid_data_handler.data["nationalLocation"],
            national_7day_infections = covid_data_handler.data["nationalLast7daysCases"],
            hospital_cases = covid_data_handler.data["currentHospitalCases"],
            deaths_total = covid_data_handler.data["totalDeaths"],
            news_articles = articles,
            updates = scheduled_updates,
            image = favicon)

    return app
    