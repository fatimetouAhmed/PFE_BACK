from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.etudiermat import etudiermats
from models.etudiermat import Etudiant
from models.etudiermat import Matiere
# from models.etudiant import Etudiant
# from models.matiere import Matiere
from schemas.etudiermat import Etudiermat


etudiermat_router=APIRouter()
@etudiermat_router.get("/matiere/{nom}")
async def matiere_id(nom:str,):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    matieres = session.query(Matiere).filter(Matiere.libelle == nom).all()
     
    # Parcourir les filières et récupérer leurs départements associés
    id=0
    for matiere in matieres:
        id=matiere.id   
    return id
@etudiermat_router.get("/")
async def read_data():
    # query =etudiermats.select()
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    result_proxy = session.query(etudiermats.c.id,etudiermats.c.id_etu,etudiermats.c.id_mat,Etudiant.prenom, Etudiant.nom, Matiere.libelle)\
               .join(Etudiant, Etudiant.id == etudiermats.c.id_etu)\
               .join(Matiere, Matiere.id == etudiermats.c.id_mat)\
               .all()
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                  "id_etu": row.id_etu,
                  "id_mat": row.id_mat,
                  "etudiant": row.prenom +' '+row.nom,
                  "matiere": row.libelle,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(etudiermats.select().fetchall())

@etudiermat_router.get("/{id}")
async def read_data_by_id(id:int,):
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    result_proxy = session.query(etudiermats.c.id,etudiermats.c.id_etu,etudiermats.c.id_mat,Etudiant.prenom, Etudiant.nom, Matiere.libelle)\
               .join(Etudiant, Etudiant.id == etudiermats.c.id_etu)\
               .join(Matiere, Matiere.id == etudiermats.c.id_mat)\
               .filter(etudiermats.c.id==id)
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                  "id_etu": row.id_etu,
                  "id_mat": row.id_mat,
                  "etudiant": row.prenom +' '+row.nom,
                  "matiere": row.libelle,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(etudiermats.select().where(etudiermats.c.id==id)).fetchall()


@etudiermat_router.post("/")
async def write_data(etudiermat:Etudiermat,):

    con.execute(etudiermats.insert().values(

        id_etu=etudiermat.id_etu,
        id_mat=etudiermat.id_mat,
        ))
    return await read_data()



@etudiermat_router.put("/{id}")
async def update_data(id:int,etudiermat:Etudiermat,):
    con.execute(etudiermats.update().values(
        id_etu=etudiermat.id_etu,
        id_mat=etudiermat.id_mat,
    ).where(etudiermats.c.id==id))
    return await read_data()

@etudiermat_router.delete("/{id}")
async def delete_data(id:int,):
    con.execute(etudiermats.delete().where(etudiermats.c.id==id))
    return await read_data()
