from pydantic import BaseModel
from datetime import datetime
class Examun(BaseModel):
   type:str
   heure_deb:datetime
   heure_fin:datetime
   id_mat:int
   id_sal:int