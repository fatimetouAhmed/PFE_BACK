from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.semestre_etudiant import semestre_etudiants
from models.semestre_etudiant import Etudiants
from models.semestre_etudiant import Semestres
# from models.etudiant import Etudiant
# from models.matiere import Matiere
from schemas.semestre_etudiant import Semestre_etudiant

semestre_etudiant_router=APIRouter()
# @semestre_etudiant_router.get("/etudiants_semestres")
# async def etudiants_semestres_data():
#     # Créer une session
#     Session = sessionmaker(bind=con)
#     session = Session()

#     # Effectuer la requête pour récupérer les étudiants avec leurs matières
#     semestre_etudiants = session.query(semestre_etudiants).options(joinedload(Etudiants.semestres,Semestres.semestres_etudiants)).all()

#     # Parcourir les étudiants et récupérer leurs matières associées
#     results = []
#     for semestre_etudiant in semestre_etudiants:
#         result = {
#             "id": semestre_etudiant.id,
#             "id_sem": semestre_etudiant.id_sem,
#             "id_etu": semestre_etudiant.id_etu,
#             "semestres": [],
#             "etudiants": [],
#         }
#         for etudiant in etudiant.etudiants:
#             result["semestres"].append({
#                 "nom": etudiant.nom,
#             })
#         for etudiant in etudiant.semestres:
#             result["etudiants"].append({
#                 "nom": semestre.nom,
#             })
#         results.append(result)

#     return results
@semestre_etudiant_router.get("/")
async def read_data(user: User = Depends(check_Adminpermissions)):
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
async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):
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
async def etudiant_id(nom:str,user: User = Depends(check_Adminpermissions)):
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
async def semestre_id(nom:str,user: User = Depends(check_Adminpermissions)):
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
async def write_data(semestre_etudiant:Semestre_etudiant,user: User = Depends(check_Adminpermissions)):

    con.execute(semestre_etudiants.insert().values(

        id_etu=semestre_etudiant.id_etu,
        id_sem=semestre_etudiant.id_sem,
        ))
    return await read_data()



@semestre_etudiant_router.put("/{id}")
async def update_data(id:int,semestre_etudiant:Semestre_etudiant,user: User = Depends(check_Adminpermissions)):
    con.execute(semestre_etudiants.update().values(
        id_etu=semestre_etudiant.id_etu,
        id_sem=semestre_etudiant.id_sem,
    ).where(semestre_etudiants.c.id==id))
    return await read_data()

@semestre_etudiant_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(semestre_etudiants.delete().where(semestre_etudiants.c.id==id))
    return await read_data()
