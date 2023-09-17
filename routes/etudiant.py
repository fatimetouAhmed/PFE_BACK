from fastapi import APIRouter,Depends,Form
from auth.authConfig import recupere_userid,create_user,read_data_users,Superviseur,Surveillant,Administrateur,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
import os
from config.db import con

from sqlalchemy import create_engine, update
from auth.authConfig import create_user,UserResponse,UserCreate,read_users_nom,superviseur_id,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from auth.authConfig import get_current_user
from schemas.etudiant import EtudiantBase
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from models.etudiant import Etudiant
from models.semestre_etudiant import Etudiants
from sqlalchemy.orm import sessionmaker, relationship, Session
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
etudiant_router=APIRouter()

@etudiant_router.get("/")
async def read_data():
    query =Etudiant.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        nom_fichier = os.path.basename(row.photo)
        result = {
                  "id": row.id,
                  "nom": row.nom,
                  "prenom": row.prenom,
                  "photo": nom_fichier,
                  "genre": row.genre,
                  "date_N": row.date_N,
                  "lieu_n": row.lieu_n,
                  "email": row.email,
                  "telephone": row.telephone,
                  "nationalite": row.nationalite,
                  "date_insecription": row.date_insecription,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(Etudiant.select().fetchall())


@etudiant_router.get("/nometudiant")
async def read_data():
    query =Etudiant.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"nom": row.nom,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
@etudiant_router.get("/etudiant_matiere")
async def afficher_data():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    etudiants = session.query(Etudiant).options(joinedload(Etudiant.matieres)).all()

    # Parcourir les étudiants et récupérer leurs matières associées
    results = []
    for etudiant in etudiants:
        result = {
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "photo": etudiant.photo,
            "genre": etudiant.genre,
            "date_N": etudiant.date_N,
            "lieu_n": etudiant.lieu_n,
            "email": etudiant.email,
            "telephone": etudiant.telephone,
            "nationalite": etudiant.nationalite,
            "date_inscription": etudiant.date_insecription,
            "matieres": []
        }
        for matiere in etudiant.matieres:
            result["matieres"].append({
                "libelle": matiere.libelle,
                "nbre_heure": matiere.nbre_heure,
                "credit": matiere.credit
            })
        results.append(result)

    return results
@etudiant_router.get("/etudiants_semestres")
async def etudiants_semestres_data():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    etudiants = session.query(Etudiants).options(joinedload(Etudiants.semestres)).all()

    # Parcourir les étudiants et récupérer leurs matières associées
    results = []
    for etudiant in etudiants:
        result = {
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "photo": etudiant.photo,
            "genre": etudiant.genre,
            "date_N": etudiant.date_N,
            "lieu_n": etudiant.lieu_n,
            "email": etudiant.email,
            "telephone": etudiant.telephone,
            "nationalite": etudiant.nationalite,
            "date_inscription": etudiant.date_insecription,
            "semestres": []
        }
        for semestre in etudiant.semestres:
            result["semestres"].append({
                "nom": semestre.nom,
                "id_fil": semestre.id_fil,
            })
        results.append(result)

    return results
@etudiant_router.get("/{id}")
async def read_data_by_id(id:int,):
    query =Etudiant.__table__.select().where(Etudiant.__table__.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"nom": row.nom,
                  "prenom": row.prenom,
                  "photo": row.photo,
                  "genre": row.genre,
                  "date_N": row.date_N,
                  "lieu_n": row.lieu_n,
                  "email": row.email,
                  "telephone": row.telephone,
                  "nationalite": row.nationalite,
                  "date_insecription": row.date_insecription,}   # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(Etudiant.select().where(Etudiant.c.id==id)).fetchall()

UPLOAD_FOLDER = Path("C:/Users/pc/StudioProjects/pfe/PFE_FRONT/images/etudiants")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
@etudiant_router.post("/")
async def write_data(nom: str= Form(...),
    prenom: str= Form(...),
    genre: str= Form(...),
    date_N: datetime= Form(...),
    lieu_n: str= Form(...),
    email: str= Form(...),
    telephone: int = Form(...),
    nationalite: str = Form(...),
    date_insecription: datetime = Form(...),file: UploadFile = File(...), user_id: int = Depends(recupere_userid), db: Session = Depends(get_db)):
    try:
        image = await file.read()      
        # Spécifiez le chemin complet du dossier où vous souhaitez stocker l'image
        upload_folder = r"C:\Users\pc\StudioProjects\pfe\PFE_FRONT\images\etudiants"
       
        # Assurez-vous que le dossier existe, sinon, créez-le
        os.makedirs(upload_folder, exist_ok=True)      
        # Générez un nom de fichier unique (par exemple, basé sur le timestamp)
        unique_filename = f"{user_id}_{datetime.now().timestamp()}.jpg"   
        # Construisez le chemin complet du fichier
        file_path = os.path.join(upload_folder, unique_filename)  
        file_path_str = str(file_path).replace("\\", "/")
        print(file_path_str)
        # Enregistrez l'image dans le dossier spécifié
        with open(file_path, "wb") as f:
            f.write(image)
        print(file_path_str)    
        # date_N = datetime.strptime('2023-09-01T22:56:45.274Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        # date_insecription = datetime.strptime('2023-09-01T22:56:45.274Z', '%Y-%m-%dT%H:%M:%S.%fZ')

        # Create a new Etudiant object
        etudiant = Etudiant(
            nom=nom,
            prenom=prenom,
            photo=str(file_path_str),
            genre=genre,
            date_N=date_N,
            lieu_n=lieu_n,
            email=email,
            telephone=telephone,
            nationalite=nationalite,
            date_insecription=date_insecription,
        )

        # Add the Etudiant object to the session and commit the changes
        db.add(etudiant)
        db.commit()

        return file_path_str
    except Exception as e:
        return {"error": str(e)}

@etudiant_router.put("/{id}")
async def update_data(id:int,nom: str= Form(...),
    prenom: str= Form(...),
    genre: str= Form(...),
    date_N: datetime= Form(...),
    lieu_n: str= Form(...),
    email: str= Form(...),
    telephone: int = Form(...),
    nationalite: str = Form(...),
    date_insecription: datetime = Form(...),file: UploadFile = File(...), user_id: int = Depends(recupere_userid), db: Session = Depends(get_db)):
    print(id)
    Session = sessionmaker(bind=con)
    session = Session()
    try:
        image = await file.read()      
        # Spécifiez le chemin complet du dossier où vous souhaitez stocker l'image
        upload_folder = r"C:\Users\pc\StudioProjects\pfe\PFE_FRONT\images\etudiants"
       
        # Assurez-vous que le dossier existe, sinon, créez-le
        os.makedirs(upload_folder, exist_ok=True)      
        # Générez un nom de fichier unique (par exemple, basé sur le timestamp)
        unique_filename = f"{user_id}_{datetime.now().timestamp()}.jpg"   
        # Construisez le chemin complet du fichier
        file_path = os.path.join(upload_folder, unique_filename)  
        file_path_str = str(file_path).replace("\\", "/")
        print(file_path_str)
        # Enregistrez l'image dans le dossier spécifié
        with open(file_path, "wb") as f:
            f.write(image)      
        update_stmt = update(Etudiant).where(Etudiant.id == id).values( nom=nom,
            prenom=prenom,
            photo=str(file_path_str),
            genre=genre,
            date_N=date_N,
            lieu_n=lieu_n,
            email=email,
            telephone=telephone,
            nationalite=nationalite,
            date_insecription=date_insecription,)
        # Execute the update statement
        session.execute(update_stmt)
        # Commit the changes
        session.commit()
        # Close the session when you're done
        session.close()
        return await read_data()
    except Exception as e:
        return {"error": str(e)}
@etudiant_router.delete("/{id}")
async def delete_data(id:int,):
    con.execute(Etudiant.__table__.delete().where(Etudiant.__table__.c.id==id))
    return await read_data()