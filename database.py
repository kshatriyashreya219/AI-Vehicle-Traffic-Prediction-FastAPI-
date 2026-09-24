import sqlite3
import os

def init_db():
    conn = sqlite3.connect("traffic.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS logs 
              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
               junction INTEGER, 
               hour INTEGER, 
               day INTEGER, 
               is_holiday INTEGER, 
               predicted_count INTEGER)""")
    conn.commit()
    conn.close()

def save_log(junction, hour, day, is_holiday, predicted_count):
    try:
        conn = sqlite3.connect("traffic.db")
        c = conn.cursor()
        c.execute("INSERT INTO logs (junction, hour, day, is_holiday, predicted_count) VALUES (?,?,?,?,?)",
                  (junction, hour, day, is_holiday, predicted_count))
        conn.commit()
        conn.close()
    except:
        pass
