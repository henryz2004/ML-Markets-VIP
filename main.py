import scraper

dbname = "data.db"

# DO NOT CREATE A DB AGAIN
# scraper.create_db(dbname)

# site:<sitename.com> is optional
prompt = "markets site:https://www.cnbc.com"
scraper.insert_into_db(scraper.news(prompt), dbname)