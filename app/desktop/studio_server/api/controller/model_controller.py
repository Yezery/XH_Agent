from fastapi import FastAPI


from ..service.llm_providers_service import LLMProviderManager,OllamaManager, get_available_models
from ...datamodel.dto.LLMdto import ConnectParams
llmProviderManager =  LLMProviderManager()
ollamaManager = OllamaManager()

def connect_provider_api(app: FastAPI):
    @app.get("/api/provider/ollama/connect")
    async def connect_ollama_api(
        custom_ollama_url: str | None = None,
    ):
        return await ollamaManager.connect_ollama(custom_ollama_url)
    
    # ================================================
    @app.post("/api/provider/llm/connect")
    async def connect_llm_api(params: ConnectParams):
        return await llmProviderManager.connect_new_api_key_provider(params.api_key,params.base_url,params.provider_name)
    
    @app.get("/api/provider/llm/disconnect")
    async def disconnect_llm(provider_name:str):
        return llmProviderManager.api_key_provider_disconnection(provider_name)
    
    @app.get("/api/provider/llm/status")
    async def connect_llm_status():
        return await llmProviderManager.loading_provider_status()
    
    @app.get("/api/provider/available_models")
    async def model_list():
        return get_available_models()
    
    