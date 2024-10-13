from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


SQLALCHEMY_DATABASE_URL = create_engine('postgresql://postgres:12345@localhost/fastapi')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
