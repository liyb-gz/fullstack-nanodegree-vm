from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	username = Column(String(60), index = True)
	email = Column(String(120))
	picture = Column(String(250))



engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)