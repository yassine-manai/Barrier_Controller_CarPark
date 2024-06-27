from ipaddress import AddressValueError, IPv4Address, IPv6Address, ip_address

from fastapi import HTTPException
from Database.db_barriers import get_db_barrier
from Models import items

def modify_barrier_rq(barrier_id: int, barrier_item: items.ModifiedBarrierItem):

    conn, cursor = get_db_barrier()

    try:
        ip = ip_address(barrier_item.ip.strip())
    except AddressValueError:   
        conn.close()
        raise HTTPException(status_code=400, detail={"errordata": 400, "message": "Invalid IP address"})

    # Normalize the IP address to ensure consistency
    if isinstance(ip, IPv4Address):
        normalized_ip = str(ip)


    cursor.execute('''UPDATE barriers SET 
                   name = ?,
                   id = ?, 
                   type = ?,
                   ip = ?, 
                   port = ?

                   WHERE id = ?''',
                (
                barrier_item.name, 
                barrier_item.id, 
                barrier_item.type, 
                normalized_ip, 
                barrier_item.port,
                barrier_id))
    conn.commit()
    conn.close()

    return barrier_item

def delete_barrier_rq(barrier_id: int):
    conn, cursor = get_db_barrier()
    cursor.execute('''DELETE FROM barriers WHERE id = ?''', (barrier_id,))
    conn.commit()
    conn.close()

    return barrier_id



