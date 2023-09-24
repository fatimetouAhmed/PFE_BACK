from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.semestre_etudiant import semestre_etudiants
from models.semestre_etudiant import Etudiants
from models.semestre_etudiant import Semestres
# from models.etudiant import Etudiant
# from models.Etudiants import Etudiants
from schemas.semestre_etudiant import Semestre_etudiant

semestre_etudiant_router=APIRouter()
@semestre_etudiant_router.get("/read")
def get_semestre_etudiants_data():
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(semestre_etudiants.c.id,
                   semestre_etudiants.c.id_etu,
                   semestre_etudiants.c.id_sem,
                   Etudiants.prenom,
                   Semestres.nom). \
        join(Etudiants, Etudiants.id == semestre_etudiants.c.id_etu). \
        join(Semestres, Semestres.id == semestre_etudiants.c.id_sem)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                       'id_etu': row.id_etu,
                       'id_sem': row.id_sem,
                       'etudiant':row.prenom,
                       'semestre': row.nom} for row in result]
    return formatted_data

@semestre_etudiant_router.get("/read/{id}")
async def read_data_by_id(id:int,):
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(semestre_etudiants.c.id,
                   semestre_etudiants.c.id_etu,
                   semestre_etudiants.c.id_sem,
                   Etudiants.prenom,
                   Semestres.nom). \
        join(Etudiants, Etudiants.id == semestre_etudiants.c.id_etu). \
        join(Semestres, Semestres.id == semestre_etudiants.c.id_sem).filter(semestre_etudiants.c.id==id)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                       'id_etu': row.id_etu,
                       'id_sem': row.id_sem,
                       'etudiant':row.prenom ,
                       'semestre': row.nom} for row in result]
    return formatted_data
@semestre_etudiant_router.get("/")
async def read_data():
    query =semestre_etudiants.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                  "id_etu": row.id_etu,
                  "id_sem": row.id_sem,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(semestre_etudiants.select().fetchall())

@semestre_etudiant_router.get("/{id}")
async def read_data_by_id(id:int,):
    query =semestre_etudiants.select().where(semestre_etudiants.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                  "id_etu": row.id_etu,
                  "id_sem": row.id_sem,}   # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(semestre_etudiants.select().where(semestre_etudiants.c.id==id)).fetchall()
@semestre_etudiant_router.get("/etudiant/{nom}")
async def etudiant_id(nom:str,):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    etudiants = session.query(Etudiants).filter(Etudiants.nom == nom).all()
     
    # Parcourir les filières et récupérer leurs départements associés
    id=0
    for etudiant in etudiants:
        id=etudiant.id   
    return id

@semestre_etudiant_router.get("/semestre/{nom}")
async def semestre_id(nom:str,):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    semestres = session.query(Semestres).filter(Semestres.nom == nom).all()
    # Parcourir les filières et récupérer leurs départements associés
    id=0
    for semestre in semestres:
        id=semestre.id   
    return id
@semestre_etudiant_router.post("/")
async def write_data(semestre_etudiant:Semestre_etudiant,):

    con.execute(semestre_etudiants.insert().values(

        id_etu=semestre_etudiant.id_etu,
        id_sem=semestre_etudiant.id_sem,
        ))
    return await read_data()



@semestre_etudiant_router.put("/{id}")
async def update_data(id:int,semestre_etudiant:Semestre_etudiant,):
    con.execute(semestre_etudiants.update().values(
        id_etu=semestre_etudiant.id_etu,
        id_sem=semestre_etudiant.id_sem,
    ).where(semestre_etudiants.c.id==id))
    return await read_data()

@semestre_etudiant_router.delete("/{id}")
async def delete_data(id:int,):
    con.execute(semestre_etudiants.delete().where(semestre_etudiants.c.id==id))
    return await read_data()
