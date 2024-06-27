from fastapi import APIRouter, HTTPException, Request
from Config.config import DEMO
from Database.Requests.req_control import Unlock_rq
from Events.Add_Events import add_unlock_event
from Models.items import send_action, send_action_with_timeout
from Config.log_config import logger

#Routing for the api endpoint
Unlock_barrier = APIRouter()

test = "Successfully OK"

TIMEOUT = 10 

@Unlock_barrier.post("/unlock/{id}", tags=["Barriers Controller"])
async def  unlock_barrier_by_id(id: int, request: Request, extradata: str = "No Extra data"):
    
    if DEMO == 1:
        return test 
    else: 
        barrier_info = Unlock_rq(id)
        status_code = 500

        if not barrier_info:
            raise HTTPException(status_code=404, detail={"errorcode": 404, "description": "Barrier not Found"})
        
        ip_address, port, hex_code = barrier_info
        logger.info(f"Barrier info: IP - {ip_address}, Port - {port}, Hex Code - {hex_code}")
        ip_user = request.client.host

        try:
            response_data = await send_action_with_timeout(ip_address, port, hex_code, 'Unlocked', timeout=TIMEOUT)
            status_code = 200

        except HTTPException as e:
            status_code = e.status_code 
            logger.error(f"HTTPException occurred: {e}")
            raise 
        
        except Exception as e:
            if "unreachable" in str(e).lower():
                logger.error(f"Barrier is unreachable: {e}")
                raise HTTPException(status_code=503, detail={"errorcode": 503, "message": "Barrier is unreachable"})
            else:
                logger.error(f"An error occurred: {e}")
                raise HTTPException(status_code=500, detail={"errorcode": 500, "message": str(e)})


        if response_data is not None:
            add_unlock_event(id, ip_user, status_code, extradata)
            return response_data
        
        else:
            raise HTTPException(status_code=500, detail={"errorcode": 500, "message": "Internal server error - No response"})


 
