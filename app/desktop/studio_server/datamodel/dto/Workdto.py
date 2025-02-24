
from fastapi import File, UploadFile
from pydantic import BaseModel



    
class ImagesTexts(BaseModel):
    imageName: str
    text:str
    
class docxCheckOption(BaseModel):
    docxCheckKey:list[str]
    
class WorkRunParams(BaseModel):
    name: str
    id: str
    course: str
    docxName: str
    summary:str
    images_texts: list[ImagesTexts]