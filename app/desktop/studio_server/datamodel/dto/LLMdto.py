from pydantic import BaseModel

class ConnectParams(BaseModel):
    api_key: str
    base_url: str
    provider_name: str

class ProvidersStatus(BaseModel):
        name: str
        id:str
        base_url: str
class ProvidersStatusParams(BaseModel): 
    providers: list[ProvidersStatus]

class ChatRequest(BaseModel):
    model: str
    provider: str
    message: str
    
