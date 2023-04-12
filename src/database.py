import sqlite3
import datetime

# Function to create the table
def create_table():
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Create the articles table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (article_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, date_inserted TEXT, date_to_publish TEXT, content TEXT, hasTweeted BOOLEAN)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to remove tweets after a period of time
delete_interval = datetime.timedelta(weeks=2)
def delete_old_rows():
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Get the current date
    today = datetime.date.today()

    # Calculate the date 
    delete_date = today - delete_interval

    # Construct the SQL query to delete rows from the articles table where the date is older than delete_date
    sql_query = "DELETE FROM articles WHERE date_to_publish IS NULL AND date_inserted < ?"
    sql_query2 = "DELETE FROM articles WHERE date_to_publish IS NOT NULL AND date_to_publish < ?"
    # Execute the SQL query with the delete_date parameter
    c.execute(sql_query, (delete_date,))
    c.execute(sql_query2, (delete_date,))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function that can be used to store information in the database
def insert_article(title, author, date_inserted, date_to_publish, content):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Insert a new row into the articles table
    c.execute("INSERT INTO articles (title, author, date_inserted, date_to_publish, content, hasTweeted) VALUES (?, ?, ?, ?, ?)",
              (title, author, date_inserted.isoformat(), date_to_publish.isoformat(), content, False))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



# Gets all the information stored about an article
def get_single_article(article_id):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Execute a SELECT query to retrieve the content of the article
    c.execute("SELECT * FROM articles WHERE article_id = ?",
              (article_id,))
    result = c.fetchone()

    # Close the connection
    conn.close()

    # Return the content of the article 
    return result

# Function that can be used to acquire content from the 
# database given certain information about an article
def get_single_article_content(article_id):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Execute a SELECT query to retrieve the content of the article
    c.execute("SELECT content FROM articles WHERE article_id = ?",
              (article_id,))
    result = c.fetchone()

    # Close the connection
    conn.close()

    # Return the content of the article 
    return result[0]

def get_all_new_articles(hasDate: bool):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    if hasDate:
        c.execute("SELECT article_id, content, date FROM articles WHERE date IS NOT NULL AND hasTweeted = FALSE")
    else:
        c.execute("SELECT article_id, content FROM articles WHERE date IS NULL AND hasTweeted = FALSE")
    results = c.fetchall()

    # Close the connection
    conn.close()

    # Return the content of the articles 
    return results



def delete_article(article_id):
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    c.execute("DELETE FROM articles WHERE article_id=?", (article_id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return result

def pick_article():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    c.execute("SELECT * FROM articles order by random()")
    result = c.fetchone()
    
    return result
    
