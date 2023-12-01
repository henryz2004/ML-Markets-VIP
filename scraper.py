import csv
import sqlite3
from crawler import database
from crawler.sandbox import realtime

def news(query):
    scraper = realtime.RealTimeScraper(query)
    return scraper.get_data()

def create_db(name):
    database.create_database(name)

def insert_into_db(list, dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    database.insert_data(list, conn, cursor)
    conn.close()

def to_csv(filename):
    database.export_to_csv(filename)

def custom_SQL(query, dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def news_to_db(query, dbname):
    insert_into_db(news(query), dbname)