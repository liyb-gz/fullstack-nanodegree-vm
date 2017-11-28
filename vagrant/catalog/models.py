from sqlalchemy import Column, Integer, String, ForeignKey
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

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key = True)
	name = Column(String(60), index = True)
	description = Column(String(5000))

	# TODO: add nullable = False to creator id after adding authentication
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

	# TODO: add nullable = False to creator id after adding authentication
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