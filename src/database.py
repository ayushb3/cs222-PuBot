import sqlite3


# Function to create the table
def create_table():
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Create the articles table if it does not exist
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (title TEXT, author TEXT, date TEXT, content TEXT)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



# Function that can be used to store information in the database
def insert_article(title, author, date, content):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Insert a new row into the articles table
    c.execute("INSERT INTO articles (title, author, date, content) VALUES (?, ?, ?, ?)",
              (title, author, date, content))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function that can be used to acquire content from the 
# database given certain information about an article
def get_article_content(title, author, date):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Execute a SELECT query to retrieve the content of the article
    c.execute("SELECT content FROM articles WHERE title = ? AND author = ? AND date = ?",
              (title, author, date))
    result = c.fetchone()

    # Close the connection
    conn.close()

    # Return the content of the article 
    return result[0]

# Gets all the information stored about an article
def get_article(title, author, date):
    # Connect to the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Execute a SELECT query to retrieve the content of the article
    c.execute("SELECT * FROM articles WHERE title = ? AND author = ? AND date = ?",
              (title, author, date))
    result = c.fetchone()

    # Close the connection
    conn.close()

    # Return the content of the article 
    return result

def pick_article():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    c.execute("SELECT * FROM articles order by random()")
    result = c.fetchone()
    
    return result
    