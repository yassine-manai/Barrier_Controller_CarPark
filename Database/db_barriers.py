from Config.config import DB_FILE_PATH_barrier
from Config.log_config import logger
import sqlite3


def get_db_barrier():
    logger.info(DB_FILE_PATH_barrier)
    conn = sqlite3.connect(DB_FILE_PATH_barrier)
    cursor = conn.cursor()
    
    # Check if the 'barriers' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='barriers'")
    table_barrier_exists = cursor.fetchone()

    # Table Barriers
    if not table_barrier_exists:
        cursor.execute('''CREATE TABLE barriers 
                            (
                                name TEXT,
                                id INTEGER,
                                type TEXT,
                                ip TEXT NOT NULL,
                                port INTEGER NOT NULL
                            )''')  
        
        conn.commit()
        logger.info("Created 'barriers' table")

    return conn, cursor
