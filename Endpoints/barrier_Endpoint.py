from ipaddress import AddressValueError, IPv4Address, ip_address
from Database.db_barriers import get_db_barrier
from Database.Requests.req_barrier import modify_barrier_rq
from Database.Requests.req_barrier import delete_barrier_rq
from Models import items
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Add_barrier = APIRouter()
Delete_barrier = APIRouter()
Barrier_List = APIRouter()
BarrierById = APIRouter()   
Modify_barrier = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"], 
    allow_headers=["Content-Type"], 
)



@Add_barrier.post("/add", tags=["Barriers Data"])
async def add_barrier(barrier_item: items.BarrierItem):
    conn, cursor = get_db_barrier()
    
    try:
        
        ip = ip_address(barrier_item.ip.strip())
    except AddressValueError:
        conn.close()
        raise HTTPException(status_code=400, detail={"errordata": 400, "message": "Invalid IP address"})

    if isinstance(ip, IPv4Address):
        normalized_ip = str(ip)


    existing_barrier = cursor.execute(
        "SELECT * FROM barriers WHERE id = ?", (barrier_item.id,)
    ).fetchone()

    if existing_barrier:
        conn.close()
        raise HTTPException(status_code=400, detail={"errordata": 404, "message": "Barrier with the same ID already exists"})

    cursor.execute(
        '''INSERT INTO barriers (name, id, type, ip, port)
           VALUES (?, ?, ?, ?, ?)''',
        (barrier_item.name, barrier_item.id, barrier_item.barrierType, normalized_ip, barrier_item.port)
    )

    conn.commit()
    conn.close()
    return {"message": "Barrier added successfully"}



@Delete_barrier.delete("/delete/{barrier_id}" , tags=["Barriers Data"])
async def delete_barrier(barrier_id: int):
    
    delete_barrier_rq(barrier_id)

    return {"message": "Barrier deleted successfully"}


@Barrier_List.get("/Barrier", tags=["Barriers Data"])
async def get_all_barriers():
    conn, cursor = get_db_barrier()
    cursor.execute('''SELECT * FROM barriers''')
    barriers = cursor.fetchall()
    conn.close()
    
    if not barriers:
        return JSONResponse(content={"barriers": []}, status_code=404)
    
    # Transform each barrier row into a dictionary representing a barrier object
    barrier_objects = []
    for barrier in barriers:
        barrier_dict = {
            "name": barrier[0],
            "id": barrier[1],
            "barrierType": barrier[2],
            "ip": barrier[3],
            "port": barrier[4]
        }
        barrier_objects.append(barrier_dict)
    
    return {"barriers": barrier_objects}



@BarrierById.get("/Barrier/{id}", tags=["Barriers Data"])
async def get_barrier_by_id(id: int):
    conn, cursor = get_db_barrier()
    cursor.execute('''SELECT * FROM barriers WHERE id = ?''', (id,))
    barrier = cursor.fetchone()
    conn.close()
    if not barrier:
        raise HTTPException(status_code=404, detail={"errordata": 404,"message":"Barrier with the same ID already exists"})
    
    barrier = {
        "name": barrier[0],
        "id": barrier[1],
        "type": barrier[2],
        "ip": barrier[3],
        "port": barrier[4],
    }

    return JSONResponse(content=barrier, status_code=200)


@Modify_barrier.put("/modify/{barrier_id}", tags=["Barriers Data"])
async def modify_barrier(barrier_id: int, barrier_item: items.ModifiedBarrierItem):

    modify_barrier_rq(barrier_id, barrier_item)
    
    return {"message": "Barrier modified successfully"}