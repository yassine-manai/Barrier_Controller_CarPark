from fastapi import APIRouter, HTTPException, Request
from Config.config import DEMO
from Database.Requests.req_control import Close_rq
from Events.Add_Events import add_close_event
from Models.items import response, send_action_with_timeout
from Config.log_config import logger

# Routing for the API endpoint
Close_barrier = APIRouter()

TIMEOUT = 10

test = "Successfully OK"

@Close_barrier.post("/close/{id}", tags=["Barriers Controller"])
async def close_barrier_by_id(request: Request, id: int, extradata: str = ""):
    

    if DEMO == 1:
        return test
    else:
        barrier_info = Close_rq(id)
        status_code = 500

        if not barrier_info:
            raise HTTPException(status_code=404, detail={"errorcode": 404, "description": "Barrier not Found"})
        
        ip_address, port, hex_code = barrier_info
        logger.info(f"Closing Barrier - IP: {ip_address}, Port: {port}, Hex Code: {hex_code}")
        ip_user = request.client.host
        
        try:
            # Attempt to close the barrier
            response_data = await send_action_with_timeout(ip_address, port, hex_code, 'Closed', timeout=TIMEOUT)
            status_code = 200  

            status_response = response(ip_address, port, hex_code, 'stat')

            if "Opened" in status_response["response"]: 
                logger.info("Barrier is open, resending close command.")
                response_data = await send_action_with_timeout(ip_address, port, hex_code, 'Closed', timeout=TIMEOUT)
            elif "Closed" in status_response["response"]:
                logger.info("Barrier is closed, no further action needed.")

        except ConnectionResetError as conn_reset_err:
            logger.error(f"Connection reset by peer while attempting to close the barrier: {conn_reset_err}")
            logger.info("Resending close command after connection reset by peer.")
            # Retry closing the barrier
            try:
                response_data = await send_action_with_timeout(ip_address, port, hex_code, 'Closed', timeout=TIMEOUT)
                status_code = 200
            except Exception as e:
                logger.error(f"Error occurred while retrying close command: {e}")
                raise HTTPException(status_code=500, detail={"errorcode": 500, "message": "Error occurred while retrying command"})
            
        except Exception as e:
            if "unreachable" in str(e).lower():
                logger.error(f"Barrier is unreachable: {e}")
                raise HTTPException(status_code=503, detail={"errordata": 503, "message": "Barrier is unreachable"})
            else:
                logger.error(f"An error occurred: {e}")
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": str(e)})

        add_close_event(id, ip_user, status_code, extradata)  # Adding event regardless of response status code

        if response_data is not None:
            return response_data
        else:
            raise HTTPException(status_code=502, detail={"errorcode": 502, "message": "Internal server error - No response"})
