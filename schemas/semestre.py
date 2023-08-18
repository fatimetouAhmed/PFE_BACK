from pydantic import BaseModel
from datetime import datetime
class SemestreBase(BaseModel):
   nom:str
   id_fil:int
   date_debut:datetime
   date_fin:datetime