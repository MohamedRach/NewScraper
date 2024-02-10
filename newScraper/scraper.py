from scraperClass import scraperClass;
import logging
import time
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BlockingScheduler
from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
import certifi

def get_past_day(unit, number):
    # Get current date
    current_date = datetime.now()
    # Define time delta based on the unit
    if unit == 'day':
        delta = timedelta(days=number)
    else:
        raise ValueError("Invalid unit. Choose 'day', 'week', 'month', or 'year'.")
    # Calculate the past date
    past_date = current_date - delta
    
    return past_date

def set_logging(): 
    # Get current time and convert to date
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f'logs/{today}.log'

    # Create an empty log file if not exist
    if not os.path.exists(log_file):
        open(log_file, 'a')
    else:
        pass
    # Set logging config
    logging.basicConfig(filename=log_file, 
                        encoding='utf-8', 
                        level=logging.INFO, 
                        filemode='a', 
                        format='%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def remove_old_log():
        # Delete logs older than 21 days
        date_delete = get_past_day('day', 21)
        log_delete = f'logs/{date_delete}.log'
        try:
            os.remove(log_delete)
        except Exception as msg:
            logging.info(f"log '{log_delete}' doesn't exist, skip delete log file!")
        else:
            logging.info(f"deleted {log_delete}!")

def job():
    newScraper = scraperClass()
    articles = []
    sources = [{
        'source': "hespressEnglish",
        "link": "https://en.hespress.com/"
    },
    {
        'source': "hespress",
        'link': 'https://www.hespress.com/'
    },
    {
        'source': "hibapress",
        'link': "https://ar.hibapress.com/mobiles.html",    
    },
    {
        'source': "lnt",
        'link': "https://lnt.ma/",
    }]
    ##set_logging()
    ##logging.info('Started crawling {}...'.format(datetime.now()))
    for source in sources:
         articles.append(newScraper.scraper(source))
    ##logging.info('Finished crawling {}...'.format(datetime.now()))
    print(articles)
    #scheduler.shutdown()

if __name__ == '__main__':
    '''
    scheduler = BlockingScheduler()
    # Running message
    print('Started application {}'.format(datetime.now()))
    print('****************************** APP IS RUNNING ******************************')
    # Run process
    scheduler.add_job(job, 'interval', minutes = 1)
    #scheduler.add_job(remove_old_log, 'interval', minutes= 1)
    scheduler.start()
    '''

    demo_table = resource('dynamodb').Table('news')

#############################  insert record #############################

    def insert():
        print(f'demo_insert')
        response = demo_table.put_item(
            Item={
                    'id': 'cus-05', # parition key
                    'title' : 'ord-5',  # sort key
                    'link': 'pending',
                    'image': 'img',
                    'created_date' : datetime.now().isoformat()
                }
            )
        print(f'Insert response: {response}') 
    
    insert()



