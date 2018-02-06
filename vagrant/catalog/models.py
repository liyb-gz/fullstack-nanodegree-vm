from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	username = Column(String(60))
	email = Column(String(120), unique = True)
	picture = Column(String(250))

	# Required by Flask_login
	gid = Column(String(20), nullable = False)
	is_authenticated = Column(Boolean)
	is_active = Column(Boolean)
	is_anonymous = Column(Boolean)

	def get_id(self):
		return self.gid

	@property
	def serialize(self):
		return {
			'id': self.id,
			'gid': self.gid,
			'username': self.username,
			'email': self.email,
			'picture': self.picture
		}

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key = True)
	name = Column(String(60), index = True)
	description = Column(String(5000))

	creator_id = Column(Integer, ForeignKey('user.id'))
	creator = relationship(User)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'creator_id': self.creator_id
		}

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key = True)
	name = Column(String(60), index = True)
	description = Column(String(5000))

	category_id = Column(Integer, ForeignKey('category.id'), nullable = False)
	category = relationship(Category)

	creator_id = Column(Integer, ForeignKey('user.id'))
	creator = relationship(User)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'category_id': self.category_id,
			'creator_id': self.creator_id
		}

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)