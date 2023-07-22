from fastapi import APIRouter
from config.db import con
from models.user import users 
from schemas.user import User

user_router=APIRouter()
@user_router.get("/")
async def read_data():
    query = users.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"id": row.id,
                  "nom": row.nom,
                   "prenom": row.prenom,
                   "email": row.email,
                   "pswd": row.pswd,
                   "role": row.role,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(users.select().fetchall())

@user_router.get("/{id}")
async def read_data_by_id(id:int):
    query = users.select().where(users.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"id": row.id,
                  "nom": row.nom,
                   "prenom": row.prenom,
                   "email": row.email,
                   "pswd": row.pswd,
                   "role": row.role,}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(users.select().where(users.c.id==id)).fetchall()

@user_router.post("/")
async def write_data(user:User):
    print("nom",user.nom)
    con.execute(users.insert().values(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        pswd=user.pswd,
        role=user.role,
        ))
    return await read_data()

@user_router.put("/{id}")
async def update_data(id:int,user:User):
    con.execute(users.update().values(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        pswd=user.pswd,
        role=user.role,
    ).where(users.c.id==id))
    return await read_data()

@user_router.delete("/{id}")
async def delete_data(id:int):
    con.execute(users.delete().where(users.c.id==id))
    return await read_data()
