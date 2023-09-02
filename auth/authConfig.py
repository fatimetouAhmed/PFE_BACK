from fastapi import Depends, FastAPI, HTTPException, status 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey ,DateTime
from sqlalchemy.orm import sessionmaker, relationship, Session
from passlib.hash import bcrypt
from sqlalchemy.orm import declarative_base 
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config.db import con
from typing import Optional


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=con)
# Create a session
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
    __tablename__ = "users"

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
    superviseur_id: Optional[int] = None  # Champ superviseur_id optionnel

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



# Fonction pour ajouter un utilisateur
def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.pswd)
    db_user = User(nom=user.nom, prenom=user.prenom, email=user.email, pswd=hashed_password, role=user.role,photo=user.photo)
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.role == "admin":
        admin = Administrateur(user_id=db_user.id)
        db.add(admin)
        db.commit()
        db.refresh(admin)
    elif user.role == "surveillant":
        superviseur_id = user.superviseur_id  # Récupération du superviseur_id depuis user
        surveillant = Surveillant(user_id=db_user.id, superviseur_id=superviseur_id)  # Utilisation du superviseur_id lors de la création du surveillant
        db.add(surveillant)
        db.commit()
        db.refresh(surveillant)
    elif user.role == "superviseur":
     superviseur = Superviseur(user_id=db_user.id)
     db.add(superviseur)
     db.commit()
     db.refresh(superviseur)

    return UserResponse(id=db_user.id, nom=db_user.nom, prenom=db_user.prenom, email=db_user.email, role=db_user.role,photo=db_user.photo)


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