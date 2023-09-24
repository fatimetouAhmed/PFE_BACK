from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import Surveillant,Superviseur,User, recupere_userid,create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.surveillance import surveillances
from models.surveillance import Surveillants
from models.surveillance import Salles
# from models.etudiant import Etudiant
# from models.matiere import Matiere
from schemas.surveillance import Surveillance

surveillance_router=APIRouter()
@surveillance_router.get("/")
async def read_data():  
    # return results
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(surveillances.c.id,
                   surveillances.c.date_debut,
                   surveillances.c.date_fin,
                   surveillances.c.surveillant_id,
                    surveillances.c.salle_id,
                   Salles.nom,
                   User.prenom). \
        join(Salles, Salles.id == surveillances.c.salle_id). \
        join(Surveillants, Surveillants.user_id == surveillances.c.surveillant_id). \
        join(User, Surveillants.user_id == User.id)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                        'date_debut': row.date_debut, 
                       'date_fin': row.date_fin,
                       'surveillant_id': row.surveillant_id,
                       'salle_id': row.salle_id,
                       'superviseur': row.prenom, 
                       'departement': row.nom, 

                       } for row in result]
    return formatted_data
    # return con.execute(surveillances.select().fetchall())
@surveillance_router.get("/surveillances/nom")
async def read_data():
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    query = session.query(User.prenom).join(Surveillant).all()
    results = []
    for row in query:
        result = {
            "prenom": row[0],
        }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)

    return results
@surveillance_router.get("/surveillances/{nom}")
async def read_data(nom:str,):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    query = session.query(Surveillant).join(User).filter(User.prenom==nom).all()
    id=0
    for surveillance in query:
        id=surveillance.user_id  
    return id

    return results
@surveillance_router.get("/surveillance")
async def read_data(user_id: int = Depends(recupere_userid), ):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()
    query = session.query(Surveillant.user_id).join(Superviseur).filter(Surveillant.superviseur_id == user_id).all()

    ids = [row[0] for row in query]  # Extract the list of IDs from the query results

    query1 = session.query(surveillances).join(Surveillants).filter(Surveillants.user_id.in_(ids)).all()
    results = []
    for row in query1:
        result = {
            "id": row.id,
            "date_debut": row.date_debut,
            "date_fin": row.date_fin,
            "surveillant_id": row.surveillant_id,
            "salle_id": row.salle_id,
        }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)

    return results


@surveillance_router.get("/{id}")
async def read_data(id:int):  
    # return results
    Session = sessionmaker(bind=con)
    session = Session()
    query = select(surveillances.c.id,
                   surveillances.c.date_debut,
                   surveillances.c.date_fin,
                   surveillances.c.surveillant_id,
                    surveillances.c.salle_id,
                   Salles.nom,
                   User.prenom). \
        join(Salles, Salles.id == surveillances.c.salle_id). \
        join(Surveillants, Surveillants.user_id == surveillances.c.surveillant_id). \
        join(User, Surveillants.user_id == User.id).filter(surveillances.c.id==id)

    result = session.execute(query).fetchall()
    formatted_data = [{'id': row.id,
                        'date_debut': row.date_debut, 
                       'date_fin': row.date_fin,
                       'surveillant_id': row.surveillant_id,
                       'salle_id': row.salle_id,
                       'superviseur': row.prenom, 
                       'departement': row.nom, 

                       } for row in result]
    return formatted_data
    # return con.execute(surveillances.select().where(surveillances.c.id==id)).fetchall()


@surveillance_router.post("/")
async def write_data(surveillance:Surveillance,):

    con.execute(surveillances.insert().values(

        date_debut=surveillance.date_debut,
        date_fin=surveillance.date_fin,     
        surveillant_id=surveillance.surveillant_id,
        salle_id=surveillance.salle_id,
        ))
    return await read_data()



@surveillance_router.put("/{id}")
async def update_data(id:int,surveillance:Surveillance,):
    con.execute(surveillances.update().values(
        date_debut=surveillance.date_debut,
        date_fin=surveillance.date_fin,     
        surveillant_id=surveillance.surveillant_id,
        salle_id=surveillance.salle_id,
    ).where(surveillances.c.id==id))
    return await read_data()

@surveillance_router.delete("/{id}")
async def delete_data(id:int,):
    con.execute(surveillances.delete().where(surveillances.c.id==id))
    return await read_data()
