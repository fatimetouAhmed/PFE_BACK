from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from schemas.etudiant import EtudiantBase
# from models.etudiant import Etudiant
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from models.etudiermat import Etudiant
from models.semestre_etudiant import Etudiants
etudiant_router=APIRouter()

@etudiant_router.get("/")
async def read_data(user: User = Depends(check_Adminpermissions)):
    query =Etudiant.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                  "id": row.id,
                  "nom": row.nom,
                  "prenom": row.prenom,
                  "photo": row.photo,
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
async def read_data(user: User = Depends(check_Adminpermissions)):
    query =Etudiant.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"nom": row.nom,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
@etudiant_router.get("/etudiant_matiere")
async def afficher_data(user: User = Depends(check_Adminpermissions)):
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
async def etudiants_semestres_data(user: User = Depends(check_Adminpermissions)):
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
async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):
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


@etudiant_router.post("/")
async def write_data(etudiants:EtudiantBase,user: User = Depends(check_Adminpermissions)):

    con.execute(Etudiant.__table__.insert().values(
        nom=etudiants.nom,
        prenom=etudiants.prenom,
        photo=etudiants.photo,
        genre=etudiants.genre,
        date_N=etudiants.date_N,
        lieu_n=etudiants.lieu_n,
        email=etudiants.email,
        telephone=etudiants.telephone,
        nationalite=etudiants.nationalite,       
        date_insecription=etudiants.date_insecription,
        ))
    return await read_data()



@etudiant_router.put("/{id}")
async def update_data(id:int,etudiants:EtudiantBase,user: User = Depends(check_Adminpermissions)):
    con.execute(Etudiant.__table__.update().values(
        nom=etudiants.nom,
        prenom=etudiants.prenom,
        photo=etudiants.photo,
        genre=etudiants.genre,
        date_N=etudiants.date_N,
        lieu_n=etudiants.lieu_n,
        email=etudiants.email,
        telephone=etudiants.telephone,
        nationalite=etudiants.nationalite,       
        date_insecription=etudiants.date_insecription,
    ).where(Etudiant.__table__.c.id==id))
    return await read_data()

@etudiant_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(Etudiant.__table__.delete().where(Etudiant.__table__.c.id==id))
    return await read_data()
