from fastapi import APIRouter,Depends
from auth.authConfig import recupere_userid,create_user,Surveillant,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.historique import Historiques 
from models.etudiermat import Etudiant
from models.examun import Matieres
from models.examun import Salle
from models.examun import examuns
from models.etudiermat import etudiermats
from models.etudiermat import Matiere
from models.surveillance import surveillances
from models.surveillance import Surveillants
from models.salle import salles
from models.surveillance import Surveillants  
from schemas.historique import Historique
from models.historique import Notifications
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from sqlalchemy import select, literal_column,column
from datetime import datetime
historique_router=APIRouter()

@historique_router.get("/historique_examun")
async def historique_departement_data(user: User = Depends(check_Adminpermissions)):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()
    # Effectuer la requête pour récupérer les filières avec leurs départements
    historiques = session.query(Historiques).join(Historiques.examuns).all()

    # Parcourir les filières et récupérer leurs départements associés
    results = []
    for historique in historiques:
        result = {
            "description": historique.description,
            "examuns": {
                "type": historique.examuns.type,
                "heure_deb": historique.examuns.heure_deb,
                "heure_fin": historique.examuns.heure_fin,
            }
        }
        results.append(result)

    return results
@historique_router.get("/historiques")
async def historiques():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    historiques = session.query(Historiques).join(Historiques.examuns).all()

    # Parcourir les filières et récupérer leurs départements associés
    results = []
    for historique in historiques:
        result = {
            "id":historique.id,
            "description": historique.description,
            "examuns": historique.examuns.type,
            "examuns_date": historique.examuns.heure_deb,
         
        }
        results.append(result)

    return results
@historique_router.get("/")
async def read_data(user: User = Depends(check_Adminpermissions)):
   
    query = Historiques.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                  "description": row.description,
                  "id_exam": row.id_exam,}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(historiques.__table__.select().fetchall())

@historique_router.get("/{id}")
async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):

    query = Historiques.__table__.select().where(Historiques.__table__.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                  "description": row.description,
                  "id_exam": row.id_exam,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(historiques.__table__.select().where(historiques.__table__.c.id==id)).fetchall()

@historique_router.post("/postcasetudiant")
async def write_data_case_etudiant(id_etu:int,user_id: int = Depends(recupere_userid),user: User = Depends(check_survpermissions)):
    date=datetime.now()
    id_super=0
    surveillant = user_id
    # print("Suveillance",surveillant)
    id_sal = 0
    salle = []
    matiere_examun = []
    etudiant = []
    a = 0
    Session = sessionmaker(bind=con)
    session = Session()
    q1 = select(column('salle_id')).select_from(surveillances).where(surveillances.c.surveillant_id == surveillant and surveillances.c.date_debut<=date and surveillances.c.date_fin>=date)
    r1 = con.execute(q1)
    for row in r1:
        id_sal = row[0]
        salle_id = row[0]
        a = salle_id
        # print(a)

    q2 = session.query(examuns.c.id_mat, Salle.nom,examuns.c.id,examuns.c.type).join(examuns).filter(Salle.id == a and examuns.c.heure_deb<=date and examuns.c.heure_fin>=date )
    r2 = q2.all()
    for row in r2:
        mat_id = row[0]
        a = mat_id
        result = {
            "id_sal": row[0],
            "libelle": row[1],
            "id_exam": row[2],
            "type": row[3],
            
        }
        salle.append(result)

    q3 = session.query(Matieres.libelle).join(examuns).filter(examuns.c.id_mat == a)
    r3 = q3.all()
    for row in r3:
        mat_id = row[0]
        a = mat_id
        result = {
            "libelle": row[0],
        }
        matiere_examun.append(result)
        # print(matiere_examun)
    q4= session.query(Etudiant.id,Etudiant.nom,Etudiant.prenom).filter(Etudiant.id == id_etu )
    r4=q4.all()

    for row in r4:

        result = {
            "id_etu" :row[0],
            "nom" : row[1],
            "prenom" : row[2],
        }
        etudiant.append(result)
    q5= session.query(Surveillant.superviseur_id).filter(Surveillant.user_id == user_id )
    r5=q5.all()

    for row in r5:
        id_super =row[0]


    # description = "Attention étudiant "+ str(etudiant[0]["nom"]) + " " + str(etudiant[0]["prenom"]) + " n'a pas d'examen en ce moment " \
    #                 "et tente d'entrer dans la salle " + str(salle[0]["libelle"]) + " pour passer l'examen " + str(salle[0]["type"]) + " dans la matière " + \
    #                 str(matiere_examun[0]["libelle"]) + " au moment "+ str(date) + ", le surveillant "+ str(surveillant) +" de la salle N°" + str(id_sal)
    description = "Attention étudiant " + str(etudiant[0]["nom"]) + " " + str(etudiant[0]["prenom"]) + " n'a pas d'examen en ce moment " \
                "et tente d'entrer dans la salle " + str(salle[0]["libelle"]) + " pour passer l'examen " + str(salle[0]["type"]) + " dans la matière " + \
                str(matiere_examun[0]["libelle"]) + " au moment " + str(date) + ", le surveillant " + str(surveillant) + " de la salle N°" + str(id_sal)

    con.execute(Historiques.__table__.insert().values(
        description=description,
        id_exam=salle[0]["id_exam"]
    ))
    # print("photo  : "+image1)
    # print("examun" + str(salle[0]["id_exam"]))
    con.execute(Notifications.__table__.insert().values(
        content=description,
        date=date,
        superviseur_id=id_super,
        is_read=False,
        id_exam=salle[0]["id_exam"],
        image="",
    ))
    return description

@historique_router.post("/")
async def write_data(user_id: int = Depends(recupere_userid),user: User = Depends(check_survpermissions)):
    date=datetime.now()
    id_super=0
    surveillant = user_id
    id_sal = 0
    salle = []
    matiere_examun = []
    a = 0
    Session = sessionmaker(bind=con)
    session = Session()
    q1 = select(column('salle_id')).select_from(surveillances).where(surveillances.c.surveillant_id == surveillant and surveillances.c.date_debut<=date and surveillances.c.date_fin>=date)
    r1 = con.execute(q1)
    for row in r1:
        id_sal = row[0]
        salle_id = row[0]
        a = salle_id
        # print(a)

    q2 = session.query(examuns.c.id_mat, Salle.nom,examuns.c.id,examuns.c.type).join(examuns).filter(Salle.id == a and examuns.c.heure_deb<=date and examuns.c.heure_fin>=date )
    r2 = q2.all()
    for row in r2:
        mat_id = row[0]
        a = mat_id
        result = {
            "id_sal": row[0],
            "libelle": row[1],
            "id_exam": row[2],
            "type": row[3],
            
        }
        salle.append(result)

    q3 = session.query(Matieres.libelle).join(examuns).filter(examuns.c.id_mat == a)
    r3 = q3.all()
    for row in r3:
        mat_id = row[0]
        a = mat_id
        result = {
            "libelle": row[0],
        }
        matiere_examun.append(result)
        # print(matiere_examun)
    q5= session.query(Surveillant.superviseur_id).filter(Surveillant.user_id == user_id )
    r5=q5.all()

    for row in r5:
        id_super =row[0]
    # print("supervieur",id_super)
    if salle and matiere_examun:
        description = "Attention, quelqu'un n'est pas reconnu par l'application, et cette personne essaie d'entrer dans " + str(salle[0]["libelle"]) +" pour passer l'examen "\
            + str(salle[0]["type"]) + " dans la matière " + \
                        str(matiere_examun[0]["libelle"]) + " au moment "+ str(date) + ", le surveillant "+ str(surveillant) +" de la salle N°" + str(id_sal)
    else:
        description = "Some default description when data is unavailable"

    # description = "Attention, quelqu'un n'est pas reconnu par l'application, et cette personne essaie d'entrer dans " + str(salle[0]["libelle"]) +" pour passer l'examen "\
    #     + str(salle[0]["type"]) + " dans la matière " + \
    #                 str(matiere_examun[0]["libelle"]) + " au moment "+ str(date) + ", le surveillant "+ str(surveillant) +" de la salle N°" + str(id_sal)

    con.execute(Historiques.__table__.insert().values(
        description=description,
        id_exam=salle[0]["id_exam"]
    ))
    # print("photo  : "+image1)
    # print("examun" + str(salle[0]["id_exam"]))
    con.execute(Notifications.__table__.insert().values(
        content=description,
        date=date,
        superviseur_id=id_super,
        is_read=False,
        id_exam=salle[0]["id_exam"],
        image="",
    ))
    return description


@historique_router.put("/{id}")
async def update_data(id:int,historique:Historique,user: User = Depends(check_Adminpermissions)):
    con.execute(Historiques.__table__.update().values(
        description=historique.description,
        id_exam=historique.id_exam,
    ).where(Historiques.__table__.c.id==id))
    return await read_data()

@historique_router.put("/{id}")
async def update_data_Notification(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(Notifications.__table__.update().values(
        is_read=True,
    ).where(Notifications.__table__.c.id==id))
    return await read_data()

@historique_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(Historiques.__table__.delete().where(Historiques.__table__.c.id==id))
    return await read_data()
