import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi_standalone_docs import StandaloneDocs
from fastapi.middleware.cors import CORSMiddleware

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from Elka.close_barrier import Close_barrier
from Elka.open_barrier import Open_barrier
from Elka.close_barrier import Close_barrier
from Elka.status_barrier import Status
from Elka.unlock_barrier import Unlock_barrier
from Elka.lock_barrier import Lock_barrier

from Endpoints.barrier_Endpoint import Add_barrier
from Endpoints.barrier_Endpoint import Delete_barrier
from Endpoints.barrier_Endpoint import Barrier_List
from Endpoints.barrier_Endpoint import BarrierById
from Endpoints.barrier_Endpoint import Modify_barrier
from Config.config import APP_PORT

from Events.Get_Events import Event_List
from Events.Get_Events import EventById
from Events.Delete_Event import Delete_all_event
from Events.Delete_Event import Delete_event

tags_metadata = [
    {
        "name": "Barriers Data",
        "description": "CRUD Operations for barriers data",
    },
    {
        "name": "Barriers Controller",
        "description": "Action for barrier: OPEN & CLOSE & LOCK & UNLOCK operations",
    },
    {
        "name": "Events",
        "description": "All Events for barrier",
    },
]


# Initialize FastAPI application
app = FastAPI(
    title="Barriers",
    openapi_tags=tags_metadata,
    redoc_url=None
)

StandaloneDocs(app=app)


templates = Environment(loader=FileSystemLoader("static"))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

# Barrier Controller Endpoints
app.include_router(Open_barrier)
app.include_router(Close_barrier)
app.include_router(Lock_barrier)
app.include_router(Unlock_barrier)
app.include_router(Status)

# Barrier Data Endpoints
app.include_router(Add_barrier)
app.include_router(BarrierById)
app.include_router(Barrier_List)
app.include_router(Modify_barrier)
app.include_router(Delete_barrier)

# Events Data Endpoints
app.include_router(Event_List)
app.include_router(EventById)
app.include_router(Delete_event)
app.include_router(Delete_all_event)

#start_websocket_server()

@app.get("/")
@app.get("/login.html", tags=["UI"], include_in_schema=False)
async def render_template(request: Request):
    try:
        template = templates.get_template("login.html")
        content = template.render(title="Login")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")
    

@app.get("/")
@app.get("/index.html", tags=["UI"], include_in_schema=False)
async def render_template(request: Request):
    try:
        template = templates.get_template("index.html")
        content = template.render(title="Welcome to Barriers")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")

@app.get("/")
@app.get("/events.html", tags=["UI"], include_in_schema=False)
async def render_template(request: Request):
    try:
        template = templates.get_template("events.html")
        content = template.render(title="Welcome to Barriers")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")

@app.get("/")
@app.get("/test.html", tags=["UI"], include_in_schema=False)
async def render_template(request: Request):
    try:
        template = templates.get_template("test.html")
        content = template.render(title="Welcome to Barriers")
        
        return HTMLResponse(content=content)
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail="Template not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=APP_PORT, reload=True)