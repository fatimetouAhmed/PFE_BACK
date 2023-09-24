from fastapi import Depends, FastAPI, HTTPException, status 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey ,DateTime
from sqlalchemy.orm import sessionmaker, relationship, Session
from passlib.hash import bcrypt
from sqlalchemy import create_engine, update
from sqlalchemy.orm import declarative_base 
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config.db import con
from typing import Optional
from fastapi import APIRouter,Depends,Form
import os
from sqlalchemy.orm import sessionmaker, relationship, Session
from fastapi import FastAPI, File, UploadFile
from datetime import datetime
user_router=APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=con)
# Create a session
#Base = declarative_base()
Base = declarative_base()

# ...
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèles de données (tables)
class User(Base):
    __tablename__ = "users"  # Spécifiez le nom de la table dans la base de données

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    pswd = Column(String(255))
    role = Column(String(255))
    photo = Column(String(250))

    surveillant = relationship("Surveillant", back_populates="user", uselist=False)
    administrateur = relationship("Administrateur", back_populates="user", uselist=False)
    superviseur = relationship("Superviseur", back_populates="user", uselist=False)


class Administrateur(Base):
    __tablename__ = "administrateurs"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="administrateur", uselist=False)


# ...
class Surveillant(Base):
    __tablename__ = "surveillants"

    #id = Column(Integer, pr
    # imary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    superviseur_id = Column(Integer, ForeignKey("superviseurs.user_id"))
    typecompte=Column(String(255), nullable=False,default="principale")
    user= relationship("User", back_populates="surveillant", uselist=False)
    superviseur = relationship("Superviseur", back_populates="surveillant", uselist=False)
    pv = relationship("PV", back_populates="surveillant", uselist=False)


class PV(Base):
    __tablename__ = "pv"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=True)
    nni = Column(String(255), nullable=True)
    surveillant_id = Column(Integer, ForeignKey("surveillants.user_id"))
    photo = Column(String(255), nullable=True)
    tel = Column(Integer, nullable=True)
    date_pv = Column(DateTime, default=datetime.now)
    surveillant = relationship("Surveillant", back_populates="pv")

class Superviseur(Base):
    __tablename__ = "superviseurs"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    #sureveillant_id = Column(Integer, ForeignKey("surveillants.user_id"))

    user = relationship("User", back_populates="superviseur", uselist=False)
    surveillant = relationship("Surveillant", back_populates="superviseur", uselist=False)

app = FastAPI()

# Modèle Pydantic pour la création d'un utilisateur
class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    pswd: str
    role: str
    photo:str
    superviseur_id:int
        # Optional[int] = None  # Champ superviseur_id optionnel

class UserResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    role: str
    photo:str

# Fonction pour hacher le mot de passe
def hash_password(password: str) -> str:
    return bcrypt.hash(password)


@user_router.post("/registeruser/")
# Fonction pour ajouter un utilisateur
async def create_user(
    nom: str = Form(...),
    prenom: str = Form(...),
    email: str = Form(...),
    pswd: str = Form(...),
    role: str = Form(...),
    superviseur_id: int = Form(...),
    file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    try:
        image = await file.read()      
        # Spécifiez le chemin complet du dossier où vous souhaitez stocker l'image
        upload_folder = r"C:\Users\pc\StudioProjects\pfe\PFE_FRONT\images\users"
        # id_surv_int=int(id_surv)
        # if id_surv == '' or id_surv is None:
        #  id_surv_int = 0
        # else:
        #    id_surv_int = int(id_surv)
     
        # Assurez-vous que le dossier existe, sinon, créez-le
        os.makedirs(upload_folder, exist_ok=True)      
        # Générez un nom de fichier unique (par exemple, basé sur le timestamp)
        unique_filename = f"{datetime.now().timestamp()}.jpg"   
        # Construisez le chemin complet du fichier
        file_path = os.path.join(upload_folder, unique_filename)  
        file_path_str = str(file_path).replace("\\", "/")
        print(file_path_str)
        # Enregistrez l'image dans le dossier spécifié
        with open(file_path, "wb") as f:
            f.write(image)
        print(file_path_str)    
        # date_N = datetime.strptime('2023-09-01T22:56:45.274Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        # date_insecription = datetime.strptime('2023-09-01T22:56:45.274Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        hashed_password = hash_password('ghhg')
        db_user = User(nom=nom, prenom=prenom, email=email, pswd=hashed_password, role=role ,photo=file_path_str)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        if role == "admin":
            admin = Administrateur(user_id=db_user.id)
            db.add(admin)
            db.commit()
            db.refresh(admin)
        elif role == "surveillant":
            superviseur_id = superviseur_id  # Récupération du superviseur_id depuis user
            surveillant = Surveillant(user_id=db_user.id, superviseur_id=superviseur_id)  # Utilisation du superviseur_id lors de la création du surveillant
            db.add(surveillant)
            db.commit()
            db.refresh(surveillant)
        elif role == "superviseur":
            superviseur = Superviseur(user_id=db_user.id)
            db.add(superviseur)
            db.commit()
            db.refresh(superviseur)

        return UserResponse(id=db_user.id, nom=db_user.nom, prenom=db_user.prenom, email=db_user.email, role=db_user.role,photo=db_user.photo)
    except Exception as e:
        return {"error": str(e)}


# Route pour créer un utilisateur
@app.post("/registeruser/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

#authentification
# ...

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ...

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class TokenData(BaseModel):
    email: str
    role: str = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.pswd):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "role": data["role"]})  # Ajout du rôle dans les données à encoder
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Fonction pour récupérer un utilisateur depuis la base de données
def get_user(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == username).first()
    db.close()
    print(user)
    return user
blacklisted_tokens = set()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
            # Vérifier si le token est dans la liste noire
        if token in blacklisted_tokens:
            raise HTTPException(status_code=401, detail="Token révoqué")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        role: str = payload.get("role")  # Récupération du rôle depuis le token
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        token_data = TokenData(email=email, role=role)  # Ajout du rôle à TokenData
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    # Vérification des autorisations
    if user.role != token_data.role:  # Vérification du rôle
        raise HTTPException(status_code=403, detail="Insufficient privileges")

    return user



#print(get_current_user)

    


# Vérifier les autorisations pour une route protégée
def check_survpermissions(user: User = Depends(get_current_user)):
    if user.role != "surveillant":
    #if user.role not in ["admin", "surveillant","superviseur"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user

def check_Adminpermissions(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user

def check_superviseurpermissions(user: User = Depends(get_current_user)):
    if user.role != "superviseur":
    #if user.role not in ["admin", "users"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user
def check_permissions(user: User = Depends(get_current_user)):
    #if user.role != "superviseur":
    if user.role not in ["admin", "superviseur"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user
def recupere_user(user: User= Depends(get_current_user)):

      user_data = {
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": user.role,
        "photo": user.photo

                 }
      return user_data
def recupere_userid(user: User = Depends(get_current_user)):
    user_data = {
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": user.role,
        "photo": user.photo

    }
    user_id = user_data["id"]
    return user_id
# @app.get("/")
async def read_data_users():
    result_proxy = con.execute(User.__table__.select())
    results = []
    for row in result_proxy:
        nom_fichier = os.path.basename(row.photo)
        result = {
            "id": row.id,
            "nom": row.nom,
            "prenom": row.prenom,
            "email": row.email,
            "role": row.role,
            "photo": nom_fichier,
        }
        results.append(result)
    return results

async def read_data_users_by_id(id:int):
    
    # query = User.__table__.
    result_proxy =     con.execute(User.__table__.select().where(User.__table__.c.id==id))
    results = []
    for row in result_proxy:
        nom_fichier = os.path.basename(row.photo)
        result = {
            "id": row.id,
            "nom": row.nom,
            "prenom": row.prenom,
            "email": row.email,
            "role": row.role,
            "photo": nom_fichier,
        }
        results.append(result)
    return results
async def superviseur_id(nom:str,user: User = Depends(check_Adminpermissions)):
    # Créer une session
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    supervi = session.query(User).filter(User.nom == nom and User.role=='superviseur').all()
     
    # Parcourir les filières et récupérer leurs départements associés
    id=0
    for supervis in supervi:
        id=supervis.id
    
    return id
async def read_users_nom():
    Session = sessionmaker(bind=con)
    session = Session()

    # Effectuer la requête pour récupérer les filières avec leurs départements
    supervi = session.query(User.nom).filter(User.role=='superviseur').all()
    results = []
    for row in supervi:
        result = {
            "nom": row.nom,
        }
        results.append(result)
    return results
@user_router.put("/{id}")
async def update_data(
    id:int,   
    nom: str = Form(...),
    prenom: str = Form(...),
    email: str = Form(...),
    pswd: str = Form(...),
    role: str = Form(...),
    superviseur_id: int = Form(...),
    file: UploadFile = File(...),):
    Session = sessionmaker(bind=con)
    session = Session()
    try:
        image = await file.read()      
        # Spécifiez le chemin complet du dossier où vous souhaitez stocker l'image
        upload_folder = r"C:\Users\pc\StudioProjects\pfe\PFE_FRONT\images\users"
       
        # Assurez-vous que le dossier existe, sinon, créez-le
        os.makedirs(upload_folder, exist_ok=True)      
        # Générez un nom de fichier unique (par exemple, basé sur le timestamp)
        unique_filename = f"{datetime.now().timestamp()}.jpg"   
        # Construisez le chemin complet du fichier
        file_path = os.path.join(upload_folder, unique_filename)  
        file_path_str = str(file_path).replace("\\", "/")
        print(file_path_str)
        # Enregistrez l'image dans le dossier spécifié
        with open(file_path, "wb") as f:
            f.write(image)
       
        update_stmt = update(User).where(User.id == id).values(
        nom=nom,
        prenom=prenom,
        email=email,
        pswd=pswd,
        role=role,
        photo=str(file_path_str)
           )

        # Execute the update statement
        session.execute(update_stmt)
        # Commit the changes
        session.commit()
        # Close the session when you're done
        session.close()
        return await read_data_users()
    except Exception as e:
        return {"error": str(e)}

@user_router.delete("/{id}")
async def delete_data(id:int,user: User = Depends(check_Adminpermissions)):
    # con.execute(Superviseur.__table__.delete().where(Superviseur.__table__.c.user_id==id))
    # con.execute(Surveillant.__table__.delete().where(Surveillant.__table__.c.user_id==id))
    # con.execute(Administrateur.__table__.delete().where(Administrateur.__table__.c.user_id==id))
    con.execute(User.__table__.delete().where(User.__table__.c.id==id))
    return await read_data_users()