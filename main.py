import scraper

dbname = "data.db"

scraper.create_db(dbname)

# site:<sitename.com> is optional
prompt = "mrkets site:https://www.cnbc.com"
scraper.insert_into_db(scraper.news(prompt), dbname)