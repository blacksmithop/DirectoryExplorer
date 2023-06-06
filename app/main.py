from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Any


app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

def https_url_for(request: Request, name: str, **path_params: Any) -> str:

    http_url = request.url_for(name, **path_params)

    # Replace 'http' with 'https'
    return http_url.replace("http", "https", 1)

templates.env.globals["https_url_for"] = https_url_for

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "path": ""})

@app.get("/{folder_name}")
async def get_directory(request: Request, folder_name: str):
    if folder_name:
        if "." in folder_name:
            return FileResponse(f"static/{folder_name}")
        return templates.TemplateResponse(f"{folder_name}/index.html", {"request": request, "path": request.url.path})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "path": ""})
    
@app.get("/{folder_name}/{file_name}")
async def get_file(request: Request, folder_name: str, file_name: str):
    return FileResponse(f"static/{folder_name}/{file_name}")