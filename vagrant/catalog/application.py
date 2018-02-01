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

	return render_template('index.html', \
		categories = [category.serialize for category in categories])

@app.route('/categories/create/', methods = ['GET', 'POST'])
def createCategory():
	""" Create a new category."""
	if request.method == 'GET':
		# display create new category page
		categories = session.query(Category).all()

		return render_template('category_create.html', \
			categories = [category.serialize for category in categories])

	elif request.method == 'POST':
		# receive data from create page form, store it to database
		data = request.form
		name = data.get('cname')
		desc = data.get('cdesc')

		if name is not None:
			newCategory = Category(name = name, description = desc)
			session.add(newCategory)
			session.commit()
			flash('New category "{}" is created.'.format(newCategory.name))
			return redirect(url_for('showAllCategories'))
		else:
			abort(400, 'The new category must have a name!')

@app.route('/categories/<int:category_id>/')
def displayOneCategory(category_id):
	""" Display a specific category.
		GET: display this category together with items belong to it.
	"""

	# Check if the category exists
	activeCategory = session.query(Category).filter_by(id = category_id).first()
	if activeCategory is not None:
		categories = session.query(Category).all()
		items = session.query(Item).filter_by(category_id = category_id).all()
		return render_template('category.html', \
			categories = [category.serialize for category in categories], \
			activeCategory = activeCategory, \
			items = items, \
			id = category_id)
	else:
		abort(404)


@app.route('/categories/<int:category_id>/update', methods = ['GET', 'POST'])
def updateCategory(category_id):
	if request.method == 'GET':
		activeCategory = session.query(Category).filter_by(id = category_id).first()
		if activeCategory is not None:
			categories = session.query(Category).all()
			return render_template('category_update.html', \
				categories = [category.serialize for category in categories], \
				activeCategory = activeCategory, \
				id = category_id)
		else:
			abort(404)

	elif request.method == 'POST':

		# receive data from create page form, store it to database
		data = request.form
		name = data.get('cname')
		desc = data.get('cdesc')

		category = session.query(Category).filter_by(id = category_id).one()

		if name is not None:
			category.name = name

		if desc is not None:
			category.description = desc
			
		session.add(category)
		session.commit()

		return redirect(url_for('displayOneCategory', category_id = category_id))

@app.route('/categories/<int:category_id>/delete', methods = ['GET', 'POST'])
def deleteCategory(category_id):
	if request.method == 'GET':
		activeCategory = session.query(Category).filter_by(id = category_id).first()
		if activeCategory is not None:
			categories = session.query(Category).all()
			return render_template('category_delete.html', \
				categories = [category.serialize for category in categories], \
				activeCategory = activeCategory, \
				id = category_id)
		else:
			abort(404)

	elif request.method == 'POST':
		category = session.query(Category).filter_by(id = category_id).one()

		session.delete(category)
		session.commit()

		return redirect(url_for('showAllCategories'))

@app.route('/categories/<int:category_id>/create', methods = ['GET', 'POST'])
def createItem(category_id):
	activeCategory = session.query(Category).filter_by(id = category_id).first()
	categories = session.query(Category).all()

	if activeCategory is not None:
		if request.method == 'GET':
				return render_template('item_create.html', \
					categories = [category.serialize for category in categories], \
					activeCategory = activeCategory, \
					id = category_id)

		elif request.method == 'POST':
			# receive data from create page form, store it to database
			data = request.form
			name = data.get('iname')
			desc = data.get('idesc')

			if name != '' and name is not None:

				newItem = Item( \
					name = name, \
					description = desc, \
					category_id = category_id)
				session.add(newItem)
				session.commit()

				items = session.query(Item).filter_by(category_id = category_id).all()

				return render_template('category.html', \
					categories = [category.serialize for category in categories], \
					activeCategory = activeCategory, \
					items = items, \
					id = category_id)

			else:
				abort(400, 'The item name must not be empty.')
	else:
		abort(404)

def updateItem():
	pass

def deleteItem():
	pass

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
