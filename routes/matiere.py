from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.etudiermat import Matiere
from models.examun import Matieres
from schemas.matiere import MatiereBase
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from sqlalchemy import select
matiere_router=APIRouter()
   
@matiere_router.get("/afficher")
async def afficher_data():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    matieres = session.query(Matiere).options(joinedload(Matiere.matieres_etudiants)).all()

    # Parcourir les étudiants et récupérer leurs matières associées
    results = []
    for matiere in matieres:
        result = {
            "libelle": matiere.libelle,
            "nbre_heure": matiere.nbre_heure,
            "credit": matiere.credit,
            "matieres_etudiants": []
        }
        for etudiant in  matiere.matieres_etudiants:
            result["matieres_etudiants"].append({
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
            })
        results.append(result)

    return results

@matiere_router.get("/matieres_salles")
async def matieres_salles_data():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les étudiants avec leurs matières
    matieres = session.query(Matieres).options(joinedload(Matieres.matieres_salles)).all()

    # Parcourir les étudiants et récupérer leurs matières associées
    results = []
    for matiere in matieres:
        result = {
            "libelle": matiere.libelle,
            "nbre_heure": matiere.nbre_heure,
            "credit": matiere.credit,
            "matieres_salles": []
        }
        for salle in  matiere.matieres_salles:
            result["matieres_salles"].append({
            "nom": salle.nom,
           
            })
        results.append(result)

    return results
@matiere_router.get("/")
async def read_data():
    query = select(Matiere) # Utilisez select(Matiere) au lieu de select([Matiere])
    matieres = con.execute(query)
 
    results = []
    for matiere in matieres:
        result = {
             "id": matiere.id,
            "libelle": matiere.libelle,
            "nbre_heure": matiere.nbre_heure,
            "credit": matiere.credit
        }
        results.append(result)

    return results
@matiere_router.get("/nom")
async def read_data():
    query = select(Matiere) # Utilisez select(Matiere) au lieu de select([Matiere])
    matieres = con.execute(query)
 
    results = []
    for matiere in matieres:
        result = {
            "libelle": matiere.libelle,
        }
        results.append(result)

    return results
    # return con.execute(matieres.select().fetchall())

@matiere_router.get("/{id}")
async def read_data_by_id(id:int,):
    query = Matiere.__table__.select().where(Matiere.__table__.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"libelle": row.libelle,
                  "nbre_heure": row.nbre_heure,
                  "credit": row.credit}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(matieres.select().where(matieres.c.id==id)).fetchall()

@matiere_router.post("/")
async def write_data(matieres:MatiereBase,):
    # print("nom",matiere.nom)
    con.execute(Matiere.__table__.insert().values(
        libelle=matieres.libelle,
        nbre_heure=matieres.nbre_heure,
        credit=matieres.credit
        ))
    return await read_data()

@matiere_router.put("/{id}")
async def update_data(id:int,matieres:MatiereBase,):
    con.execute(Matiere.__table__.update().values(
        libelle=matieres.libelle,
        nbre_heure=matieres.nbre_heure,
        credit=matieres.credit
    ).where(Matiere.__table__.c.id==id))
    return await read_data()

@matiere_router.delete("/{id}")
async def delete_data(id:int,):
    con.execute(Matiere.__table__.delete().where(Matiere.__table__.c.id==id))
    return await read_data()
