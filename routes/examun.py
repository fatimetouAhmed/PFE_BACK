from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_permissions,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.examun import examuns
from models.examun import Salle,Matieres
# from models.examun import Salle
# from models.examun import Matieres
# from models.etudiant import Etudiant
# from models.matiere import Matiere
from schemas.examun import Examun

examun_router=APIRouter()
@examun_router.get("/salle/{nom}")
async def salle_id(nom:str):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    salles = session.query(Salle).filter(Salle.nom == nom).all()
     
    # Parcourir les filières et récupérer leurs départements associés
    id=0
    for salle in salles:
        id=salle.id   
    return id
@examun_router.get("/matiere/{nom}")
async def matiere_id(nom:str):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    matieres = session.query(Matieres).filter(Matieres.libelle == nom).all()
     
    # Parcourir les filières et récupérer leurs départements associés
    id=0
    for matiere in matieres:
        id=matiere.id   
    return id
@examun_router.get("/examun/nom")
async def examun_nom():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    exs = session.query(examuns.c.id,examuns.c.type).all()
     
    # Parcourir les filières et récupérer leurs départements associés
    examun = []
    for ex in exs:
        noms = {
            "id":ex.id,
            "type": ex.type  
        }
        examun.append(noms)
    return examun

@examun_router.get("/")
async def read_data():
    Session = sessionmaker(bind=con)
    session = Session()
    result_proxy = session.query(examuns.c.id,examuns.c.type,examuns.c.heure_deb,examuns.c.heure_fin,examuns.c.id_mat,examuns.c.id_sal,Matieres.libelle, Salle.nom)\
               .join(Matieres, Matieres.id == examuns.c.id_mat)\
               .join(Salle, Salle.id == examuns.c.id_sal)\
               .all()
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                 "type": row.type,
                  "heure_deb": row.heure_deb,
                  "heure_fin": row.heure_fin,
                "id_mat": row.id_mat,
                  "id_sal": row.id_sal,
                   "matiere": row.libelle,
                    "salle": row.nom,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(examuns.select().fetchall())

@examun_router.get("/{id}")
async def read_data_by_id(id:int):
    Session = sessionmaker(bind=con)
    session = Session()
    result_proxy = session.query(examuns.c.id,examuns.c.type,examuns.c.heure_deb,examuns.c.heure_fin,examuns.c.id_mat,examuns.c.id_sal,Matieres.libelle, Salle.nom)\
               .join(Matieres, Matieres.id == examuns.c.id_mat)\
               .join(Salle, Salle.id == examuns.c.id_sal)\
               .filter(examuns.c.id==id)
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                 "type": row.type,
                  "heure_deb": row.heure_deb,
                  "heure_fin": row.heure_fin,
                  "id_mat": row.id_mat,
                  "id_sal": row.id_sal,
                   "matiere": row.libelle,
                    "salle": row.nom,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(examuns.select().where(examuns.c.id==id)).fetchall()


@examun_router.post("/")
async def write_data(examun:Examun,):

    con.execute(examuns.insert().values(
        type=examun.type,
        heure_deb=examun.heure_deb,
        heure_fin=examun.heure_fin,
        id_sal=examun.id_sal,
        id_mat=examun.id_mat,
        ))
    return await read_data()



@examun_router.put("/{id}")
async def update_data(id:int,examun:Examun,):
    con.execute(examuns.update().values(
        type=examun.type,
        heure_deb=examun.heure_deb,
        heure_fin=examun.heure_fin,
        id_sal=examun.id_sal,
        id_mat=examun.id_mat,
    ).where(examuns.c.id==id))
    return await read_data()

@examun_router.delete("/{id}")
async def delete_data(id:int,):
    con.execute(examuns.delete().where(examuns.c.id==id))
    return await read_data()
