from pydantic import BaseModel

class User(BaseModel):
   nom:str
   prenom:str
   email:str
   pswd:str
   role:str