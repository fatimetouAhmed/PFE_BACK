from pydantic import BaseModel
from datetime import datetime

class EtudiantBase(BaseModel):
    nom: str
    prenom: str
    # photo: str
    genre: str
    date_N: datetime
    lieu_n: str
    email: str
    telephone: int
    nationalite: str
    date_insecription: datetime
