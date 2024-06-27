import sqlite3
from Config.config import DB_FILE_PATH_events
from Config.log_config import logger

MAX_ROWS = 1000

def get_db_events():
    logger.info(DB_FILE_PATH_events)
    conn = sqlite3.connect(DB_FILE_PATH_events)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    table_event_exists = cursor.fetchone()

    # Table Events
    if not table_event_exists:
        cursor.execute('''CREATE TABLE events 
                            (
                                barrier_id INTEGER,
                                time TEXT,
                                extraData TEXT,
                                ip_user TEXT,
                                meth TEXT
                            )'''
                       )
        
        conn.commit()
        logger.info("Created 'events' table")
    else:
        logger.info("Events table already exists")
    
    cursor.execute("SELECT COUNT(*) FROM events")
    current_row_count = cursor.fetchone()[0]
    if current_row_count >= MAX_ROWS:
        cursor.execute("DELETE FROM events")
        conn.commit()
        logger.info("Deleted all rows from 'events' table as it reached the maximum limit")
    
    return conn, cursor
