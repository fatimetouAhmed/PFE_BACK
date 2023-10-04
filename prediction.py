from PIL import Image
from io import BytesIO
import deepface
from deepface import DeepFace
from pydantic import BaseModel
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String ,Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dbconfig import get_etudiant ,get_infoexamun
from routes.historique import write_data
from fastapi import APIRouter,Depends
from auth.authConfig import recupere_userid,create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
import os
from datetime import datetime, timedelta

models = [
          "VGG-Face", 
          "Facenet", 
          "Facenet512", 
          "OpenFace", 
          "DeepFace", 
          "DeepID", 
          "ArcFace", 
          "Dlib", 
          "SFace",
            ]

async def predict_face(image_path,user_id: int = Depends(recupere_userid),user: User = Depends(check_survpermissions)):
  
        print( "test",image_path)
        
        results = DeepFace.find(img_path =image_path, db_path = "C:/Users/pc/StudioProjects/pfe/PFE_FRONT/images/etudiants",model_name=models[1],enforce_detection=False)
    #    print("---------------------------"+pathi+"--------------------------------")
        
        try:
            # print("resultats", results)
            photo = list(map(lambda x: x['identity'], results))
            if len(photo) <= 0:
                raise Exception("Étudiant inexistant")
            else:
                if len(photo[0]) > 0:
                    url = photo[0][0]
                    image_name = os.path.basename(url)
                    # print(image_name)
                    print("url:", url)
                    id = get_etudiant(url)
                    donne = await get_infoexamun(image_path,image_name, id, user_id, user)
                    return donne
                else:
                    raise Exception("Étudiant inexistant")
        except Exception as e:
            url = photo[0][0] if len(photo) > 0 and len(photo[0]) > 0 else None
            timestamp = datetime.now().timestamp()
            notification_filename = f"{timestamp}.jpg"
                
            notification_folder = "C:/Users/pc/StudioProjects/pfe/PFE_FRONT/images/notifications"
            notification_path = os.path.join(notification_folder, notification_filename)
            os.rename(image_path, notification_path)
            
            # Appelez la fonction write_data avec l'URL du dossier "notifications"
            image_etu_url = notification_path.replace("\\", "/")
            print("exception")
            result = await write_data(image_etu_url,user_id, user,)
            return result

      

      #  except Exception as e:
      #   return {"etudiant n existe pas"}
       #else:
     #    return 'etudiant n existe pas' 
 
    
    # Convertir la série en objet JSON
    #data_json = data.to_json(orient='values')
    #res=data_json.replace(" \ ", "")
     # result1= result.to_json()
    #if data_json is None:
     #   return {"error": "No face detected in the image"}