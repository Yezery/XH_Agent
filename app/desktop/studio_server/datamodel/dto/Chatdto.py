from pydantic import BaseModel


class Chatdto(BaseModel):
    promt: str = ""
    stream: bool = True
    temperature: float = 0.6
    top_p: float = 0.95
    not_history: bool = False
    history_id: str = ""
