from pydantic import BaseModel
from datetime import datetime
class Surveillance(BaseModel):
   date_debut:datetime
   date_fin:datetime
   surveillant_id:int
   salle_id:int