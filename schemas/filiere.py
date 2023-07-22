from pydantic import BaseModel

class Filiere(BaseModel):
   nom:str
   description:str
   id_dep:int