from pydantic import BaseModel

class SemestreBase(BaseModel):
   nom:str
   id_fil:int