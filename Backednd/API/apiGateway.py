from fastapi import FastAPI, Form ,File, UploadFile
import uvicorn
from pydantic import BaseModel

class apiGateway:
    services=[]
    endpoints=[]
    def __init__(self,i_services,i_endpoints,):
        self.services=i_services
        self.endpoint=i_endpoints

    def invoke_command():
        pass