from models import User, Base, Category, Item
from flask import Flask, jsonify, request, redirect, \
				  url_for, abort, g, flash, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
@app.route('/categories/')
def showAllCategories():
	""" Homepage. 
	GET: Show all categories. 
	"""

	categories = session.query(Category).all()

	return render_template('whole_files/index.html', 
		categories = [category.serialize for category in categories])

@app.route('/categories/create/', methods = ['GET', 'POST'])
def createCategory():
	""" Create a new category."""

	data = request.form
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

@app.route('/categories/<int:id>/', methods = ['GET', 'PUT', 'DELETE'])
def processOneCategories(id):
	""" Endpoint to a specific category.
	GET: display this category together with items belong to it.
	PUT: update this category.
	DELETE: delete this category.

	Note: POST is not allowed here. 
	Creating a new category should be done in the root endpoint.
	"""

	# Check if the category exists
	category = session.query(Category).filter_by(id = id).first()
	if category is not None:

		if request.method == 'GET':
			return displayCategory(category)

		elif request.method == 'PUT':
			data = request.form
			return updateCategory(category, data)

		elif request.method == 'DELETE':
			data = request.form
			return deleteCategory(category, data)
		else:
			# Method not allowed
			abort(405)

	else:
		abort(404)


def displayCategory(category):
	return jsonify(category.serialize)

def updateCategory(category, data):
	if data.get('name') is not None:
		category.name = data.get('name') 

	if data.get('description') is not None:
		category.description = data.get('description') 
		
	session.add(category)
	session.commit()

	return "update a category: {}".format(category.serialize)

def deleteCategory(category, data):
	session.delete(category)
	session.commit()
	return "delete a category: {}".format(category.serialize)

@app.route('/json')
@app.route('/categories/json')
def jsonAllCategories():
	""" JSON Entry. Return all categories """
	categories = session.query(Category).all()
	return jsonify(categories = [category.serialize for category in categories])

@app.route('/categories/<int:category_id>/json')
def jsonCategory(category_id):
	""" JSON Entry. Return a specific categories with its items. """
	category = session.query(Category).filter_by(id = category_id).first()

	if category is not None:
		return jsonify(category = category.serialize)

	else:
		return jsonify(error = "Category not found.")


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'Secret Key'
    app.run(host='0.0.0.0', port=8000)
