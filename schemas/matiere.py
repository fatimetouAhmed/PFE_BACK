from pydantic import BaseModel

class MatiereBase(BaseModel):
   libelle:str
   nbre_heure:int
   credit:int 

