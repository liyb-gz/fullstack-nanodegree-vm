from models import User, Base, Category, Item
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/categories/', methods = ['GET', 'POST'])
def showAllCategories():
	""" Homepage. 
	GET: Show all categories. 
	POST: Create a new category."""
	if request.method == 'GET':
		return 'Show all categories. '
	elif request.method == 'POST':
		return createCategory()

def createCategory():
	return 'Create new category'

@app.route('/json')
def jsonAllCategories():
	""" JSON Entry. Return all categories with its items. """
	return jsonify(message = 'JSON Entry.')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
