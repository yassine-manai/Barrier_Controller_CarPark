from Database.db_events import get_db_events

def add_open_event_rq(barrier_id: int, ip_user: str, status_code: int, extradata: str = " "):
    status = {
        500: "Barrier Disconnected - Open Event",
        404: "Barrier Not Found - Open Event",
        200: "Barrier Opened"
    }

    conn, cursor = get_db_events()
    meth = status.get(status_code, "Unknown")
    cursor.execute('''INSERT INTO events (barrier_id, time, extradata, ip_user, meth)
                      VALUES (?, datetime('now', 'localtime'), ?, ?, ?)''', (barrier_id, extradata, ip_user, meth))
    conn.commit()
    conn.close()


def add_close_event_rq(barrier_id: int, ip_user: str, status_code: int, extradata: str = " "):
    status = {
        500: "Barrier Disconnected - Open Event",
        404: "Barrier Not Found - Open Event",
        200: "Barrier Closed"  
    }

    conn, cursor = get_db_events()
    meth = status.get(status_code, "Unknown")
    cursor.execute('''INSERT INTO events (barrier_id, time, extradata, ip_user, meth)
                      VALUES (?, datetime('now', 'localtime'), ?, ?, ?)''', (barrier_id, extradata, ip_user, meth))
    conn.commit()
    conn.close()


def delete_event_rq(barrier_id: int):
    conn, cursor = get_db_events()
    cursor.execute('''DELETE FROM events WHERE barrier_id = ?''', (barrier_id,))
    conn.commit()
    conn.close()

    return barrier_id


def delete_event_rqall():
    conn, cursor = get_db_events()
    cursor.execute('''DELETE FROM events''')
    conn.commit()
    conn.close()
