from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.filieresmatieres import filieresmatieres
from models.filieresmatieres import Matiere
from models.filieresmatieres import Filieres
# from models.etudiant import Etudiant
# from models.matiere import Matiere
from schemas.filieresmatieres import FilieresMatieres
from sqlalchemy.orm import selectinload, aliased, subqueryload
from sqlalchemy.sql import func

filieresmatieres_router=APIRouter()
@filieresmatieres_router.get("/read")
def get_filieresmatieres_data(user: User = Depends(check_superviseurpermissions)):
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(filieresmatieres.c.id,
                   filieresmatieres.c.id_mat,
                   filieresmatieres.c.id_fil,
                   Matiere.libelle,
                   Filieres.nom). \
        join(Matiere, Matiere.id == filieresmatieres.c.id_mat). \
        join(Filieres, Filieres.id == filieresmatieres.c.id_fil)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                       'id_mat': row.id_mat,
                       'id_fil': row.id_fil,
                       'matiere_libelle': row.libelle, 
                       'filiere_nom': row.nom} for row in result]
    return formatted_data
@filieresmatieres_router.get("/{id}")
def get_filieresmatieres_data(id:int,user: User = Depends(check_superviseurpermissions)):
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(filieresmatieres.c.id,
                   filieresmatieres.c.id_mat,
                   Matiere.libelle,). \
        join(Matiere, Matiere.id == filieresmatieres.c.id_mat). \
        join(Filieres, Filieres.id == filieresmatieres.c.id_fil).filter(Filieres.id==id)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                       'id_mat': row.id_mat,
                       'matieres': row.libelle,} for row in result]
    return formatted_data
# Utilisation de la fonction pour afficher les données
# data = get_filieresmatieres_data()
# for row in data:
#      print(f"ID: {row['id']}, Matière: {row['matiere_libelle']}, Filière: {row['filiere_nom']}")
@filieresmatieres_router.get("/")
async def read_data(user: User = Depends(check_Adminpermissions)):
    query =filieresmatieres.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                  "id_mat": row.id_mat,
                  "id_fil": row.id_fil,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(filieresmatieres.select().fetchall())

# @filieresmatieres_router.get("/{id}")
# async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):
#     query =filieresmatieres.select().where(filieresmatieres.c.id==id)
#     result_proxy = con.execute(query)   
#     results = []
#     for row in result_proxy:
#         result = {
#                   "id_mat": row.id_mat,
#                   "id_fil": row.id_fil,}   # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
#         results.append(result)
    
#     return results
#     # return con.execute(filieresmatieres.select().where(filieresmatieres.c.id==id)).fetchall()


@filieresmatieres_router.post("/")
async def write_data(filieresmatiere:FilieresMatieres,user: User = Depends(check_Adminpermissions)):

    con.execute(filieresmatieres.insert().values(

        id_mat=filieresmatiere.id_mat,
        id_fil=filieresmatiere.id_fil,
        ))
    return await read_data()



@filieresmatieres_router.put("/{id}")
async def update_data(id:int,filieresmatiere:FilieresMatieres,user: User = Depends(check_Adminpermissions)):
    con.execute(filieresmatieres.update().values(
        id_mat=filieresmatiere.id_mat,
        id_fil=filieresmatiere.id_fil,
    ).where(filieresmatieres.c.id==id))
    return await read_data()

@filieresmatieres_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(filieresmatieres.delete().where(filieresmatieres.c.id==id))
    return await read_data()
