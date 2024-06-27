from fastapi import APIRouter, HTTPException, Request
from Config.config import DEMO
from Database.Requests.req_control import Open_rq
from Events.Add_Events import add_open_event
from Models.items import response, send_action_with_timeout
from Config.log_config import logger

# Routing for the API endpoint
Open_barrier = APIRouter()

test = "Successfully Opened"

TIMEOUT = 10

@Open_barrier.post("/open/{id}", tags=["Barriers Controller"])
async def open_barrier_by_id(id: int, request: Request, extradata: str = " "):

    if DEMO == 1:
        return test
    else : 
        barrier_info = Open_rq(id)
        status_code = 500

        if not barrier_info:
            raise HTTPException(status_code=404, detail={"errordata": 404, "message": "Barrier not Found"})

        ip_address, port, hex_code = barrier_info
        logger.info(f"Barrier info: IP - {ip_address}, Port - {port}, Hex Code - {hex_code}")
        ip_user = request.client.host

        try:
            # Attempt to open the barrier
            response_data = await send_action_with_timeout(ip_address, port, hex_code, 'Opened', timeout=TIMEOUT)
            status_code = 200

            status_response = response(ip_address, port, hex_code, "Status")

            if "Closed" in status_response["response"]:
                logger.info("Barrier is closed, resending open command.")
                response_data = await send_action_with_timeout(ip_address, port, hex_code, 'Opened', timeout=TIMEOUT)
                
            elif "Opened" in status_response["response"]:
                logger.info("Barrier is open, no further action needed.")
                
        except ConnectionResetError as conn_reset_err:
            logger.error(f"Connection reset by peer while attempting to open the barrier: {conn_reset_err}")
            logger.info("Resending open command after connection reset by peer.")

            try:
                response_data = await send_action_with_timeout(ip_address, port, hex_code, 'Opened', timeout=TIMEOUT)
                status_code = 200

            except Exception as e:
                logger.error(f"Error occurred while retrying open command: {e}")
                raise HTTPException(status_code=500, detail={"errorcode": 500, "message": "Error occurred while retrying command"})

        except Exception as e:
            if "unreachable" in str(e).lower():
                logger.error(f"Barrier is unreachable: {e}")
                raise HTTPException(status_code=503, detail={"errordata": 503, "message": "Barrier is unreachable"})
            else:
                logger.error(f"An error occurred: {e}")
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": str(e)})

        if response_data is not None:
            add_open_event(id, ip_user, status_code, extradata)
            return response_data
        else:
            raise HTTPException(status_code=502, detail={"errordata": 502, "message": "Internal server error - No response"})