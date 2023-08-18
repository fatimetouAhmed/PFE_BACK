from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_permissions,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.filiere import Filieres 
from models.filiere import Departements 
from schemas.filiere import Filiere
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
filiere_router=APIRouter()
@filiere_router.get("/filiere_departement")
async def filiere_departement_data(user: User = Depends(check_permissions)):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    filieres = session.query(Filieres).join(Filieres.departements).all()

    # Parcourir les filières et récupérer leurs départements associés
    results = []
    for filiere in filieres:
        result = {
             "id": filiere.id,
            "nom": filiere.nom,
            "description": filiere.description,
            "id_dep": filiere.id_dep,
            "departement":  filiere.departements.nom
           
        }
        results.append(result)

    return results

@filiere_router.get("/{id}")
async def filiere_departement_data_by_id_dep(id:int,user: User = Depends(check_permissions)):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    filieres = session.query(Filieres).join(Filieres.departements).filter(Filieres.id_dep==id).all()

    # Parcourir les filières et récupérer leurs départements associés
    results = []
    for filiere in filieres:
        result = {
             "id": filiere.id,
            "nom": filiere.nom,
            "description": filiere.description,
            "id_dep": filiere.id_dep,
           
        }
        results.append(result)

    return results
@filiere_router.get("/nomfiliere")
async def read_data(user: User = Depends(check_Adminpermissions)):
    query = Filieres.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"nom": row.nom}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
@filiere_router.get("/{nom}")
async def departement_id(nom:str,user: User = Depends(check_Adminpermissions)):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    departements = session.query(Departements).filter(Departements.nom == nom).all()
     
    # Parcourir les filières et récupérer leurs départements associés
    id=0
    for departement in departements:
        id=departement.id
    
    return id
# @filiere_router.get("/departement")
# async def read_departement():
#     query = Departements.__table__.select()
#     result_proxy = con.execute(query)   
#     results = []
#     for row in result_proxy:
#         result = {
#                  "nom": row.nom,
#                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
#         results.append(result)
    
#     return results
@filiere_router.get("/")
async def read_data(user: User = Depends(check_Adminpermissions)):
    query = Filieres.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                "id": row.id,
                 "nom": row.nom,
                  "description": row.description,
                  "id_dep": row.id_dep
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(Filieres.__table__.select().fetchall())

# @filiere_router.get("/{id}")
# async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):
#     query = Filieres.__table__.select().where(Filieres.__table__.c.id==id)
#     result_proxy = con.execute(query)   
#     results = []
#     for row in result_proxy:
#         result = {"nom": row.nom,
#                   "description": row.description,
#                   "id_dep": row.id_dep}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
#         results.append(result)
    
#     return results
    # return con.execute(Filieres.__table__.select().where(Filieres.__table__.c.id==id)).fetchall()

@filiere_router.post("/")
async def write_data(filiere:Filiere):
    print("nom",filiere.nom)
    con.execute(Filieres.__table__.insert().values(
        nom=filiere.nom,
        description=filiere.description,
        id_dep=filiere.id_dep
        ))
    return await read_data()

@filiere_router.put("/{id}")
async def update_data(id:int,filiere:Filiere):
    con.execute(Filieres.__table__.update().values(
        nom=filiere.nom,
        description=filiere.description,
        id_dep=filiere.id_dep
    ).where(Filieres.__table__.c.id==id))
    return await read_data()

@filiere_router.delete("/{id}")
async def delete_data(id:int):
    con.execute(Filieres.__table__.delete().where(Filieres.__table__.c.id==id))
    return await read_data()
