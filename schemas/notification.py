from datetime import datetime
from pydantic import BaseModel

class Notification(BaseModel):
   content:str
   date:datetime
   is_read:bool
   