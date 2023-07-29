import time

import requests
import sqlite3


# Function to fetch data from Hacker News API
def get_hacker_news_data():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from Hacker News API. Status Code: {response.status_code}")
        return []


# Function to fetch individual news item details from the API
def get_news_item(item_id):
    url = f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch news item with ID {item_id}. Status Code: {response.status_code}")
        return None


# Function to create an SQLite database table to store the news data
def create_database_table():
    connection = sqlite3.connect('hacker_news.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT
        )
    ''')
    connection.commit()
    connection.close()


# Function to add news data to the SQLite database
def insert_news_data(news_data):
    connection = sqlite3.connect('hacker_news.db')
    cursor = connection.cursor()
    cursor.executemany('INSERT INTO news (id, title, url) VALUES (?, ?, ?)', news_data)
    connection.commit()
    connection.close()


def start_scrap_data():
    """
    Scrapping the top news from hacker news api and store them to database.
    :return:
    """
    # Fetch top news IDs from Hacker News API
    news_ids = get_hacker_news_data()

    # Create the database table if it doesn't exist
    create_database_table()

    # Fetch news item details and store them in a list
    news_data = []
    for item_id in news_ids:
        item = get_news_item(item_id)
        if item and 'title' in item and 'url' in item:
            news_data.append((item_id, item['title'], item['url']))
    time.sleep(5)

    # Insert news data into the database
    insert_news_data(news_data)
    print("Data insertion into the SQLite database is complete.")
