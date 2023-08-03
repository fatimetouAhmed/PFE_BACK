from fastapi import APIRouter,Depends
from auth.authConfig import create_user,UserResponse,UserCreate,get_db,authenticate_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,check_Adminpermissions,check_superviseurpermissions,check_survpermissions,User
from config.db import con
from models.departement import Departements
from schemas.departement import Departement
departement_router=APIRouter()
@departement_router.get("/")
async def read_data():
    query = Departements.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"id": row.id,
                  "nom": row.nom}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
@departement_router.get("/nomdepartement")
async def read_data(user: User = Depends(check_Adminpermissions)):
    query = Departements.__table__.select()
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {
                  "nom": row.nom}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(departement.select().fetchall())

@departement_router.get("/{id}")
async def read_data_by_id(id:int,user: User = Depends(check_Adminpermissions)):
    query = Departements.__table__.select().where(Departements.__table__.c.id==id)
    result_proxy = con.execute(query)   
    results = []
    for row in result_proxy:
        result = {"nom": row.nom}  # Créez un dictionnaire avec la clé "nom" et la valeur correspondante
        results.append(result)
    
    return results
    # return con.execute(departement.select().where(departement.c.id==id)).fetchall()

@departement_router.post("/")
async def write_data(departement:Departement,user: User = Depends(check_Adminpermissions)):
    print("nom",departement.nom)
    con.execute(Departements.__table__.insert().values(
        nom=departement.nom
        ))
    return await read_data()

@departement_router.put("/{id}")
async def update_data(id:int,departement:Departement,user: User = Depends(check_Adminpermissions)):
    con.execute(Departements.__table__.update().values(
        nom=departement.nom
    ).where(Departements.__table__.c.id==id))
    return await read_data()

@departement_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    con.execute(Departements.__table__.delete().where(Departements.__table__.c.id==id))
    return await read_data()
