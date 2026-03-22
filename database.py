import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="safespace_db"
    )
   
# Inside database.py
def save_moderation_log(post, sentiment, verdict):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SANITIZE: Ensure sentiment is clean and short
    # This prevents the "Data too long" error forever
    clean_sentiment = str(sentiment)[:50].strip().upper()
    
    query = "INSERT INTO moderation_logs (post_text, sentiment, verdict) VALUES (%s, %s, %s)"
    cursor.execute(query, (post, clean_sentiment, verdict))
    conn.commit()
    cursor.close()
    conn.close()