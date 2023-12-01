import time
import scraper
import schedule

dbname = "data.db"

def job(prompt, dbname):
    print("Running job...")
    data_to_insert = scraper.news(prompt)
    scraper.insert_into_db(data_to_insert, dbname)

def schedule_task(prompt, dbname, seconds):
    schedule.every(seconds).seconds.do(job, prompt=prompt, dbname=dbname)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Example usage:
prompt = "markets site:https://www.cnbc.com"
seconds_interval = 3600 

# schedule_task(prompt, dbname, seconds_interval)
