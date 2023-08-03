from pydantic import BaseModel
from datetime import datetime
class DepartementsSuperviseurs(BaseModel):
   id_sup:int
   id_dep:int
   date:datetime