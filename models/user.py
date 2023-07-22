from sqlalchemy import Table,Column,String,Integer
from config.db import meta

users=Table(
    'users',meta,
    Column('id',Integer,primary_key=True),
    Column('nom',String(250)),
    Column('prenom',String(250)),
    Column('email',String(250)),
    Column('pswd',String(250)),
    Column('role',String(250)),
)