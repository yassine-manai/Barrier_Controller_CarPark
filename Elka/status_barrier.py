from fastapi import APIRouter, HTTPException
from Config.config import DEMO
from Database.Requests.req_control import status_rq
from Models.items import response

Status = APIRouter()

test = "GOOOD"

@Status.get("/status/{id}", tags=["Barriers Controller"])
async def get_status(id: int):

    if DEMO == 1:
        return test
    
    else:
        hex_code = "55 02 02 02 65 FE"
        
        barrier_info = status_rq(id)

        if not barrier_info:
            raise HTTPException(status_code=404, detail={"errorcode": 404,"message":"Barrier Not found"})
        
        ip_address, port = barrier_info

        status_response = response(ip_address, port, hex_code, "Status")

        status_codes = {
            "550a070000071000000000007d4f": "Opened",
            "550a0700000720000000000052c3": "Closed",
            "550a070000071000020000009027": "Locked",
        }

        response_code = status_response["response"]
        status_description = status_codes.get(response_code, "unlocked")

        if status_description == "unlocked":
            return status_description
        elif status_description not in ["Opened", "Closed", "Locked"]:
            return "Error Occured"
        else:
            return status_description
