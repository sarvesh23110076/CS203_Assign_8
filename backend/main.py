from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import requests

app=FastAPI()

class Document(BaseModel):
    document:str

elasticsearch_url="http://elasticsearch:9200/documents/_doc"

@app.post("/insert")
def insert_document(doc:Document):
    data={"text":doc.document}
    response=requests.post(elasticsearch_url,json=data)
    if response.status_code==201:
        return {"message":"Document inserted successfully"}
    raise HTTPException(status_code=500,detail="Failed to insert document")
@app.get("/get")
def get_best_document():
    query={
        "query":{
            "match_all":{}
        },
        "size":1
    }
    search_url="http://elasticsearch:9200/documents/_search"
    response=requests.get(search_url,json=query)

    if response.status_code==200:
        data=response.json()
        if data["hits"]["hits"]:
            best_doc=data["hits"]["hits"][0]["_source"]
            return {"best_document":best_doc}
        return {"message":"No documents found"}
    
    raise HTTPException(status_code=500,detail="Failed to retrive document")
