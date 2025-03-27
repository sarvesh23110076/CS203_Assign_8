from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import requests

app=FastAPI()

backendurl="http://34.100.196.170:9567"
templates=Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def serve_home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/insert")
def insert_document(document:str=Form(...)):
    response=requests.post(f"{backendurl}/insert",json={"document":document})
    return response.json()

@app.get("/get")
def get_best_document():
    response=requests.get(f"{backendurl}/get")
    return response.json()
