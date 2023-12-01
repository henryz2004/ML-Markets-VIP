import sqlite3
import csv

def create_database(db_name='example.db'):
    """
    Create an SQLite database.

    Parameters:
    - db_name (str): The name of the SQLite database.

    Returns:
    - connection (sqlite3.Connection): SQLite database connection.
    - cursor (sqlite3.Cursor): SQLite database cursor.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            publish_date TEXT,
            url TEXT
        )
    ''')

    connection.commit()
    return connection, cursor

def insert_data(data_list, connection, cursor):
    """
    Insert a list of data into the SQLite database.

    Parameters:
    - data_list (list): List of dictionaries, each containing data to be inserted.
    - connection (sqlite3.Connection): SQLite database connection.
    - cursor (sqlite3.Cursor): SQLite database cursor.
    """
    for data in data_list:
        cursor.execute('''
            INSERT INTO articles (title, description, publish_date, url) VALUES (?, ?, ?, ?)
        ''', (data['title'], data['description'], data['publish_date'], data['url']))

    connection.commit()

def export_to_csv(db_name='example.db', csv_name='exported_data.csv'):
    """
    Export data from SQLite database to a CSV file.

    Parameters:
    - db_name (str): The name of the SQLite database.
    - csv_name (str): The name of the CSV file.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM articles')
    data = cursor.fetchall()

    with open(csv_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id', 'title', 'description', 'publish_date', 'url'])
        csv_writer.writerows(data)

    connection.close()

# Example usage:
data_list = [
    {
        "title": "Article 1",
        "description": "This is the first article.",
        "publish_date": "2023-01-01",
        "url": "http://example.com/article1"
    },
    {
        "title": "Article 2",
        "description": "This is the second article.",
        "publish_date": "2023-01-02",
        "url": "http://example.com/article2"
    },
    {
        "title": "Article 3",
        "description": "This is the third article.",
        "publish_date": "2023-01-03",
        "url": "http://example.com/article3"
    }
]