from typing import Any, List
import httpx
from pydantic import BaseModel
import requests

from app.desktop.studio_server.utils.config import Config
from app.desktop.studio_server.utils.R import error, success
from openai import OpenAI

from app.desktop.studio_server.utils.config import Config
import requests
avaluable_models = {"ollama":[]}
class LLMProviderManager:
    
    support_llm_providers = [
        {
            "name": "deepseek",
            "base_url": "https://api.deepseek.com",
        },
        {
            "name": "openAi",
            "base_url": "https://api.chatanywhere.tech/v1",
        },
        {
            "name": "qwen",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        },
        {
            "name": "siliconflow",
            "base_url": "https://api.siliconflow.cn/v1",
        },
        {
            "name": "moonshot",
            "base_url": "https://api.moonshot.cn/v1",
        },
        {
            "name": "hunyuan",
            "base_url": "https://api.hunyuan.cloud.tencent.com/v1",
        }
    ]
    
    class api_key_provider:
        clients:OpenAI
        models:list[str]
        def __init__(self,client:OpenAI,models:list[str]):
            self.clients = client
            self.models = models
    
    clients:dict[str,api_key_provider]={}

    async def get_api_key_provider_connection(self,base_url: str, api_key: str ,provider_name:str):
        if api_key == '' or api_key == None:
            return {
            "provider": provider_name,
            "message": "连接失败",
            "status":False
        }
        # 创建OpenAI客户端
        try:
            client = OpenAI(api_key=api_key, base_url=base_url,timeout=10)
            # 获取可用模型列表
            response = client.models.list()
            allModels = [model.id for model in response.data]
            # 保存设置
            Config.shared().save_setting(provider_name,api_key)
            # 将客户端和可用模型列表保存到self.clients中
            self.clients[provider_name] = self.api_key_provider(client,allModels)
            # 如果provider_name为deepseek，则将可用模型列表中的deepseek-chat替换为DeepSeek-V3，其他模型替换为DeepSeek-R1
            if provider_name == "deepseek":
                t = []
                for model in allModels:
                    if model == "deepseek-chat":
                        t.append("DeepSeek-V3")
                    else:
                        t.append("DeepSeek-R1")
                avaluable_models[provider_name] = t
            else:
                avaluable_models[provider_name] = allModels
        except Exception as e:
            print(e)
            avaluable_models[provider_name] = []
            return {
            "provider": provider_name,
            "message": "连接失败",
            "status":False
        }
        return {
            "provider": provider_name,
            "message": "连接成功",
            "status":True
        }

    def api_key_provider_disconnection(self,provider_name:str):
        if provider_name in self.clients:
            del self.clients[provider_name]
            Config.shared().save_setting(provider_name,"")
            return True
        return False
    
    async def connect_new_api_key_provider(self,api_key: str, base_url: str, provider_name: str):
        return await self.get_api_key_provider_connection(base_url,api_key,provider_name)

    async def loading_provider_status(self):
        statusList = []
        try:
            for provider in self.support_llm_providers:
                status= await self.get_api_key_provider_connection(provider["base_url"],Config.shared().get(provider["name"]),provider["name"])
                statusList.append(status)
        except Exception as e:
            print(e)
        finally:
            return success(
                data = statusList
            )
    def get_clients(self):
        return self.clients



class OllamaManager:
    class OllamaConnection(BaseModel):
        message: str
        models: List[str]

        def all_models(self) -> List[str]:
            return self.models

    def ollama_base_url(self) -> str:
        config_base_url = Config.shared().ollama_base_url
        if config_base_url:
            return config_base_url
        return "http://localhost:11434"


    async def ollama_online(self) -> bool:
        try:
            httpx.get(self.ollama_base_url() + "/api/tags")
        except httpx.RequestError:
            return False
        return True


    async def connect_ollama(self,custom_ollama_url: str | None = None) -> OllamaConnection:
        if (
            custom_ollama_url
            and not custom_ollama_url.startswith("http://")
            and not custom_ollama_url.startswith("https://")
        ):
            raise error(
                status_code=400,
                message="错误的 Ollama URL. 开头必须 http:// 或 https://",
                error="ConnectionError"
            )
        try:
            base_url = custom_ollama_url or self.ollama_base_url()
            tags = requests.get(base_url + "/api/tags", timeout=5).json()
        except requests.exceptions.ConnectionError:
            raise error(
                status_code=417,
                message="连接失败，请检查 Ollama 是否正在运行",
                error="ConnectionError"
            )
        except Exception as e:
            raise error(
                status_code=500,
                message=f"系统错误: {e}",
            )
        ollama_connection = self.parse_ollama_tags(tags)
        
        if ollama_connection is None:
            raise error(
                status_code=500,
                message="解析错误，请检查 Ollama 的响应",
            )
            
        if custom_ollama_url and custom_ollama_url != Config.shared().ollama_base_url:
            Config.shared().save_setting("ollama_base_url", custom_ollama_url)
        
        avaluable_models["ollama"] =ollama_connection.all_models()
        
        return ollama_connection

    def parse_ollama_tags(self,tags: Any) -> OllamaConnection | None:
        if "models" in tags:
            models = tags["models"]
            if isinstance(models, list):
                model_names = [model["model"] for model in models]
            return self.OllamaConnection(
                message="Ollama is running",
                models=model_names,
            )
        return None


    def ollama_model_installed(self,conn: OllamaConnection, model_name: str) -> bool:
        all_models = conn.all_models()
        return model_name in all_models or f"{model_name}:latest" in all_models
    

def get_available_models():
    return avaluable_models




