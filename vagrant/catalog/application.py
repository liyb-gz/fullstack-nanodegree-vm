from models import User, Base, Category, Item
from flask import Flask, jsonify, request, redirect, \
				  url_for, abort, g, flash
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
		return displayCategories()
	elif request.method == 'POST':
		data = request.form
		return createCategory(data)

def displayCategories():
	categories = session.query(Category).all()
	output = ''
	for category in categories:
		output += 'Category: {} \n'.format(category.name) + \
				  'Description: {} \n\n'.format(category.description)

	return output

def createCategory(data):
	name = data.get('name')
	desc = data.get('description')

	if name is not None:
		newCategory = Category(name = name, description = desc)
		session.add(newCategory)
		session.commit()
		flash('New category "{}" is created.'.format(newCategory.name))
		return redirect(url_for('showAllCategories'))
	else:
		abort(400, 'The new category must have a name!')

@app.route('/json')
def jsonAllCategories():
	""" JSON Entry. Return all categories with its items. """
	categories = session.query(Category).all()
	return jsonify(categories = [category.serialize for category in categories])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'Secret Key'
    app.run(host='0.0.0.0', port=8000)
