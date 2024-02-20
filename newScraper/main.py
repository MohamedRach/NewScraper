from scraperClass import scraperClass;
import logging
import time
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BlockingScheduler
from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key

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
        open(log_file, 'a+')
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
    set_logging()
    logging.info('Started crawling {}...'.format(datetime.now()))
    for source in sources:
         articles.append(newScraper.scraper(source))
    logging.info('Finished crawling {}...'.format(datetime.now()))
    
    
    RequestItems={
        'news': []
    }
    
    logging.info('Started inserting {}...'.format(datetime.now()))
    
    with demo_table.batch_writer() as batch:
        for arts in articles:
            for article in arts:
                article_id = article.get("id")  # Assuming "id" is the key attribute name
                if not article_id:
                    continue  # Skip if article has no ID

                # Check if the item with the same ID already exists in the table
                response = demo_table.get_item(Key={"id": article_id})

                if "Item" not in response:
                    # Item doesn't exist, so we can insert it
                    batch.put_item(Item=article)
                else:
                    # Item with the same ID already exists, so skip insertion
                   logging.info(f"Skipping insertion of duplicate item with ID: {article_id}")
    
    
    logging.info('Finished inserting {}...'.format(datetime.now()))
    remove_old_log()
    #scheduler.shutdown()

if __name__ == '__main__':
    
    demo_table = resource('dynamodb', region_name='eu-north-1', aws_access_key_id="AKIATCKAOJYWWYLXJNKS", aws_secret_access_key="").Table('news')
    scheduler = BlockingScheduler()
    # Running message
    print('Started application {}'.format(datetime.now()))
    print('****************************** APP IS RUNNING ******************************')
    # Run process
    scheduler.add_job(job, 'cron', hour=12)
    #scheduler.add_job(remove_old_log, 'interval', minutes= 1)
    scheduler.start()
    
                   
    

    


