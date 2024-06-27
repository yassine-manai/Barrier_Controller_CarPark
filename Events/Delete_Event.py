from Database.Requests.req_Event import delete_event_rq, delete_event_rqall
from fastapi import APIRouter

Delete_event = APIRouter()
Delete_all_event = APIRouter()


@Delete_event.delete("/deleteEvent/{barrier_id}" , tags=["Events"])
async def delete_event(barrier_id: int):
    
    delete_event_rq(barrier_id)

    return {"message": "Event deleted successfully"}


@Delete_all_event.delete("/deleteEvent" , tags=["Events"])
async def delete_all_events():
    
    delete_event_rqall()

    return {"message": "All events deleted successfully"}