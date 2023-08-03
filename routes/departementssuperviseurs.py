from sqlalchemy import select, join, alias
from sqlalchemy.orm import selectinload,joinedload,sessionmaker
from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.departementssuperviseurs import departementssuperviseurs

# from models.etudiant import Etudiant
# from models.matiere import Matiere
from schemas.departementssuperviseurs import DepartementsSuperviseurs


departementssuperviseurs_router=APIRouter()
@departementssuperviseurs_router.get("/")
async def read_data(user: User = Depends(check_Adminpermissions)):
    query =departementssuperviseurs.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                  "id_sup": row.id_sup,
                  "id_dep": row.id_dep,
                  "date": row.date,
                  }  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(departementssuperviseurs.select().fetchall())

@departementssuperviseurs_router.get("/{id}")
async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):
    query =departementssuperviseurs.select().where(departementssuperviseurs.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                 "id": row.id,
                  "id_sup": row.id_sup,
                  "id_dep": row.id_dep,
                  "date": row.date,
                  }   # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(departementssuperviseurs.select().where(departementssuperviseurs.c.id==id)).fetchall()


@departementssuperviseurs_router.post("/")
async def write_data(departementssuperviseur:DepartementsSuperviseurs,user: User = Depends(check_Adminpermissions)):

    con.execute(departementssuperviseurs.insert().values(

        id_sup=departementssuperviseur.id_sup,
        id_dep=departementssuperviseur.id_dep,
        date=departementssuperviseur.date,
        ))
    return await read_data()



@departementssuperviseurs_router.put("/{id}")
async def update_data(id:int,departementssuperviseur:DepartementsSuperviseurs,user: User = Depends(check_Adminpermissions)):
    con.execute(departementssuperviseurs.update().values(
        id_sup=departementssuperviseur.id_sup,
        id_dep=departementssuperviseur.id_dep,
        date=departementssuperviseur.date,
    ).where(departementssuperviseurs.c.id==id))
    return await read_data()

@departementssuperviseurs_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(departementssuperviseurs.delete().where(departementssuperviseurs.c.id==id))
    return await read_data()
