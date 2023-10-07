from fastapi import APIRouter,Depends
# from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.salle import salles
from schemas.salle import SalleBase
from models.examun import Salle
from models.surveillance import Salles
from sqlalchemy.orm import selectinload,joinedload,sessionmaker

salle_router=APIRouter()
@salle_router.get("/surveillance_salle")
async def afficher_data():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    salles = session.query(Salles).options(joinedload(Salles.surveillances_salles)).all()

    # Parcourir les étudiants et récupérer leurs matières associées
    results = []
    for salle in salles:
        result = {
            "nom": salle.nom,
            "surveillances": []
        }
        for surveillance in salle.surveillances_salles:
            result["surveillances"].append({
                "user_id": surveillance.user_id,
            })
        results.append(result)

    return results
@salle_router.get("/matieres_salles")
async def matieres_salles_data():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    salles = session.query(Salle).options(joinedload(Salle.matieres)).all()

    # Parcourir les étudiants et récupérer leurs matières associées
    results = []
    for salle in salles:
        result = {
            "nom": salle.nom,
            "matieres": []
        }
        for matiere in  salle.matieres:
            result["matieres"].append({
            "libelle": matiere.libelle,
            "nbre_heure": matiere.nbre_heure,
            "credit": matiere.credit,
            })
        results.append(result)

    return results
@salle_router.get("/")
async def read_data():
    query = salles.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"id": row.id,
                  "nom": row.nom}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
@salle_router.get("/nom")
async def read_data():
    query = salles.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                  "nom": row.nom}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(salle.select().fetchall())

@salle_router.get("/{id}")
async def read_data_by_id(id:int,):
    query = salles.select().where(salles.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"nom": row.nom}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(salle.select().where(salle.c.id==id)).fetchall()

@salle_router.post("/")
async def write_data(salle:SalleBase,):
    con.execute(salles.insert().values(
        nom=salle.nom
        ))
    return await read_data()

@salle_router.put("/{id}")
async def update_data(id:int,salle:SalleBase,):
    con.execute(salles.update().values(
        nom=salle.nom
    ).where(salles.c.id==id))
    return await read_data()

@salle_router.delete("/{id}")
async def delete_data(id:int,):
    con.execute(salles.delete().where(salles.c.id==id))
    return await read_data()
