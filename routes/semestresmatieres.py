from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_permissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.semestresmatieres import semestresmatieres
from models.semestresmatieres import Matiere
from models.semestresmatieres import Semestres
# from models.etudiant import Etudiant
# from models.matiere import Matiere
from schemas.semestresmatieres import SemestresMatieres
from sqlalchemy.orm import selectinload, aliased, subqueryload
from sqlalchemy.sql import func

semestresmatieres_router=APIRouter()
@semestresmatieres_router.get("/read")
def get_semestresmatieres_data(user: User = Depends(check_superviseurpermissions)):
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(semestresmatieres.c.id,
                   semestresmatieres.c.id_mat,
                   semestresmatieres.c.id_sem,
                   Matiere.libelle,
                   Semestres.nom). \
        join(Matiere, Matiere.id == semestresmatieres.c.id_mat). \
        join(Semestres, Semestres.id == semestresmatieres.c.id_sem)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                       'id_mat': row.id_mat,
                       'id_sem': row.id_sem,
                       'matiere_libelle': row.libelle, 
                       'filiere_nom': row.nom} for row in result]
    return formatted_data
@semestresmatieres_router.get("/{id}")
def get_semestresmatieres_data(id:int,user: User = Depends(check_permissions)):
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(semestresmatieres.c.id,
                   semestresmatieres.c.id_mat,
                   Matiere.libelle,). \
        join(Matiere, Matiere.id == semestresmatieres.c.id_mat). \
        join(Semestres, Semestres.id == semestresmatieres.c.id_sem).filter(Semestres.id==id)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                       'id_mat': row.id_mat,
                       'matieres': row.libelle,} for row in result]
    return formatted_data
# Utilisation de la fonction pour afficher les données
# data = get_semestresmatieres_data()
# for row in data:
#      print(f"ID: {row['id']}, Matière: {row['matiere_libelle']}, Filière: {row['filiere_nom']}")
@semestresmatieres_router.get("/")
async def read_data(user: User = Depends(check_Adminpermissions)):
    query =semestresmatieres.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                  "id_mat": row.id_mat,
                  "id_sem": row.id_sem,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(semestresmatieres.select().fetchall())

# @semestresmatieres_router.get("/{id}")
# async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):
#     query =semestresmatieres.select().where(semestresmatieres.c.id==id)
#     result_proxy = con.execute(query)   
#     results = []
#     for row in result_proxy:
#         result = {
#                   "id_mat": row.id_mat,
#                   "id_sem": row.id_sem,}   # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
#         results.append(result)
    
#     return results
#     # return con.execute(semestresmatieres.select().where(semestresmatieres.c.id==id)).fetchall()


@semestresmatieres_router.post("/")
async def write_data(semestresmatiere:SemestresMatieres,user: User = Depends(check_Adminpermissions)):

    con.execute(semestresmatieres.insert().values(

        id_mat=semestresmatiere.id_mat,
        id_sem=semestresmatiere.id_sem,
        ))
    return await read_data()



@semestresmatieres_router.put("/{id}")
async def update_data(id:int,semestresmatiere:SemestresMatieres,user: User = Depends(check_Adminpermissions)):
    con.execute(semestresmatieres.update().values(
        id_mat=semestresmatiere.id_mat,
        id_sem=semestresmatiere.id_sem,
    ).where(semestresmatieres.c.id==id))
    return await read_data()

@semestresmatieres_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(semestresmatieres.delete().where(semestresmatieres.c.id==id))
    return await read_data()
