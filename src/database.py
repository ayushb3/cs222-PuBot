import sqlite3


# Function to create the table
def create_table():
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Create the articles table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (article_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, date TEXT, content TEXT, hasTweeted BOOLEAN)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



# Function that can be used to store information in the database
def insert_article(title, author, date, content):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Insert a new row into the articles table
    c.execute("INSERT INTO articles (title, author, date, content, hasTweeted) VALUES (?, ?, ?, ?, ?)",
              (title, author, date, content, False))

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
    
