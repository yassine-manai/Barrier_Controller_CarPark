import binascii
from pydantic import BaseModel
from fastapi import HTTPException
from Config.log_config import logger
import socket

class BarrierItem(BaseModel):
    name:str
    id: int
    barrierType:str
    ip: str
    port: int = 52719


class ModifiedBarrierItem(BaseModel):
    name:str
    id: int
    type:str
    ip: str
    port: int



def send_action(ip_address, port, hex_code, action):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip_address, port))
            except ConnectionRefusedError as conn_refused_error:
                error_msg = f"Connection refused to {ip_address}:{port}: {str(conn_refused_error)}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
            except Exception as conn_error:
                error_msg = "errordata:501"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": "error establish connection with the barrier"})
                
            hex_bytes = bytes.fromhex(hex_code)
            
            s.sendall(hex_bytes)
            
            logger.info(f"Action '{hex_code}' sent to {ip_address}:{port}")
        
        return {"message": f"Barrier {action} with {ip_address}:{port} using {hex_code}"}
    
    except Exception as e:
        logger.error(f"Error sending Action '{hex_code}' to {ip_address}:{port}: {str(e)}")
        raise HTTPException(status_code=500, detail={"errordata": 500,"message":  'error sending action to the barrier'})
    

async def send_action_with_timeout(ip_address, port, hex_code, action, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)

            try:
                s.connect((ip_address, port))
            except ConnectionRefusedError as conn_refused_error:
                error_msg = f"Connection refused to {ip_address}:{port}: {str(conn_refused_error)}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
            except Exception as conn_error:
                error_msg = f"Error establishing connection to {ip_address}:{port}: {str(conn_error)}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
                
            hex_bytes = bytes.fromhex(hex_code)
            
            s.sendall(hex_bytes)
            
            logger.info(f"Action '{hex_code}' sent to {ip_address}:{port}")
        
        return {"message": f"Barrier {action} with {ip_address}:{port} using {hex_code}"}
    
    except Exception as e:
        logger.error(f"Error sending Action '{hex_code}' to {ip_address}:{port}: {str(e)}")
        raise HTTPException(status_code=500, detail={"errordata": 500, "message": "error sending action to the barrier"})
    


def response(ip_address, port, hex_code, action):
    BUFFER_SIZE = 1024
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip_address, port))
            except ConnectionRefusedError as conn_refused_error:
                error_msg = f"Connection refused to {ip_address}:{port}: {str(conn_refused_error)}"
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
            
            except Exception as conn_error:
                error_msg = f"Error establishing connection to {ip_address}:{port}: {str(conn_error)}"
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
                
            hex_bytes = bytes.fromhex(hex_code)
            
            s.sendall(hex_bytes)

            s.settimeout(5) 
            
            try:
                data = s.recv(BUFFER_SIZE)
                rec_data = binascii.hexlify(data).decode('utf-8')
                
                print(f"data received is {rec_data}")

                print(f"Action '{hex_code}' sent to {ip_address}:{port}")

                return {"message": f"Barrier {action} with {ip_address}:{port} using {hex_code}", "response": rec_data}
            except socket.timeout:
                error_msg = f"Timeout occurred while waiting for response from {ip_address}:{port}"
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
            except Exception as recv_error:
                error_msg = f"Error receiving response from {ip_address}:{port}: {str(recv_error)}"
                raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
    
    except Exception as e:
        error_msg = f"Error sending Action '{hex_code}' to {ip_address}:{port}: {str(e)}"
        raise HTTPException(status_code=500, detail={"errordata": 500, "message": error_msg})
