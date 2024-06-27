from Database.db_barriers import get_db_barrier

def barrier_request(id: int, cmd: str):
    conn, cursor = get_db_barrier()
    cursor.execute('''SELECT ip, port, ? FROM barriers WHERE id = ?''', (cmd, id,))
    barrier_info = cursor.fetchone()
    conn.close()
    return barrier_info

def status_request(id: int):
    conn, cursor = get_db_barrier()
    cursor.execute('''SELECT ip, port FROM barriers WHERE id = ?''', (id,))
    barrier_info = cursor.fetchone()
    conn.close()
    return barrier_info

op_cmd: str = "55 03 01 01 00 B8 B4"
cl_cmd: str = "55 03 01 02 00 ED E7"
lk_cmd: str = "55 03 01 01 01 A8 95"
uk_cmd: str = "55 03 01 01 02 98 F6"
st_cmd: str = "55 02 02 02 65 FE"

def Open_rq(id: int):
    return barrier_request(id, op_cmd)

def Close_rq(id: int):
    return barrier_request(id, cl_cmd)

def Lock_rq(id: int):
    return barrier_request(id, lk_cmd)

def Unlock_rq(id: int):
    return barrier_request(id, uk_cmd)

def status_rq(id: int):
    return status_request(id)
