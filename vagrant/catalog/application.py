# Basic FLASK functions
from flask import Flask, jsonify, request, redirect, \
				  url_for, abort, g, flash, render_template

# SQLAlchemy functions
from models import User, Base, Category, Item
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

# Session
from flask import session as login_session
import os, string

# Google Auth
from google.oauth2 import id_token
from google.auth.transport import requests

# Flask Login
from flask_login import LoginManager, login_required, \
						login_user, logout_user, current_user 

# Initialize Database
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
app = Flask(__name__)

# Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(gid):
	return session.query(User).filter_by(gid = gid).first()

CLIENT_ID = '673274558455-it6s06htmm3quqakc97q2a3bnggend4m.apps.googleusercontent.com'

@app.route('/')
@app.route('/categories/')
@login_required
def showAllCategories():
	""" Display homepage. 

	GET: Show all categories. 
	"""

	categories = session.query(Category).filter_by(\
		creator_id = current_user.id).all()

	return render_template('index.html', \
		categories = [category.serialize for category in categories])

@app.route('/categories/create/', methods = ['GET', 'POST'])
@login_required
def createCategory():
	""" Create a new category.
	
	GET: Display the "create category" page.
	POST: Accept the form from "create category" page,
		  create the category accordingly and save it to database.
	"""

	if request.method == 'GET':
		# display create new category page
		categories = session.query(Category).filter_by(\
			creator_id = current_user.id).all()

		return render_template('category_create.html', \
			categories = [category.serialize for category in categories])

	elif request.method == 'POST':
		# receive data from create page form, store it to database
		data = request.form
		name = data.get('cname')
		desc = data.get('cdesc')

		if name is not None:
			newCategory = Category(\
				name = name, \
				description = desc, \
				creator_id = current_user.id)

			session.add(newCategory)
			session.commit()

			flash('New category "{}" is created.'\
				.format(newCategory.name), 'success')

			return redirect(url_for('showAllCategories'))
		else:
			abort(400, 'The new category must have a name!')

@app.route('/categories/<int:category_id>/')
@login_required
def displayOneCategory(category_id):
	""" Display a specific category.

	GET: display this category together with items belong to it.
	"""

	# Check if the category exists
	activeCategory = session.query(Category).filter_by(\
		id = category_id, \
		creator_id = current_user.id).first()

	if activeCategory is not None:
		categories = session.query(Category).filter_by(\
			creator_id = current_user.id).all()

		items = session.query(Item).filter_by(\
			category_id = category_id, 
			creator_id = current_user.id).all()

		return render_template('category.html', \
			categories = [category.serialize for category in categories], \
			activeCategory = activeCategory, \
			items = items, \
			id = category_id)

	else:
		abort(404)


@app.route('/categories/<int:category_id>/update', methods = ['GET', 'POST'])
@login_required
def updateCategory(category_id):
	""" Update a specific category.

	GET: Display the "update category" page.
	POST: Accept the form from "update category" page,
		  update that specific category accordingly and save it to database.
	"""

	if request.method == 'GET':
		activeCategory = session.query(Category).filter_by(\
			id = category_id, \
			creator_id = current_user.id).first()

		if activeCategory is not None:
			categories = session.query(Category).filter_by(\
				creator_id = current_user.id).all()

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

		try:
			category = session.query(Category).filter_by(\
				id = category_id, \
				creator_id = current_user.id).one()

		except Exception, error:
			abort(400, str(error))

		if name is not None:
			category.name = name

		if desc is not None:
			category.description = desc
			
		session.add(category)
		session.commit()

		flash('Category "{}" is updated.'.format(category.name), 'success')

		return redirect(url_for('displayOneCategory', category_id = category_id))

@app.route('/categories/<int:category_id>/delete', methods = ['GET', 'POST'])
@login_required
def deleteCategory(category_id):
	""" Delete a specific category.

	GET: Display the "delete category" page.
	POST: Accept the form from "delete category" page,
		  delete that specific category accordingly and save it to database.
	"""

	if request.method == 'GET':
		activeCategory = session.query(Category).filter_by(\
			id = category_id, \
			creator_id = current_user.id).first()

		if activeCategory is not None:
			categories = session.query(Category).filter_by(\
				creator_id = current_user.id).all()

			return render_template('category_delete.html', \
				categories = [category.serialize for category in categories], \
				activeCategory = activeCategory, \
				id = category_id)

		else:
			abort(404)

	elif request.method == 'POST':
		try:
			category = session.query(Category).filter_by(\
				id = category_id, \
				creator_id = current_user.id).one()

			items = session.query(Item).filter_by(\
				category_id = category_id, \
				creator_id = current_user.id).all()

		except Exception, error:
			abort(400, str(error))

		session.delete(category)

		# Delete related items
		for item in items:
			session.delete(item) 
		
		session.commit()

		flash('Category "{}" is deleted.'.format(category.name), 'success')

		return redirect(url_for('showAllCategories'))

@app.route('/categories/<int:category_id>/create', methods = ['GET', 'POST'])
@login_required
def createItem(category_id):
	""" Create a new item under the given category.
	
	GET: Display the "create item" page.
	POST: Accept the form from "create item" page,
		  create the item accordingly and save it to database.
	"""

	activeCategory = session.query(Category).filter_by(\
		id = category_id, \
		creator_id = current_user.id).first()

	categories = session.query(Category).filter_by(\
		creator_id = current_user.id).all()

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
					category_id = category_id, \
					creator_id = current_user.id)
				session.add(newItem)
				session.commit()

				flash('Item "{}" is created.'.format(newItem.name), 'success')

				return redirect(url_for('displayOneCategory', \
					category_id = category_id))

			else:
				abort(400, 'The item name must not be empty.')
	else:
		abort(404)

@app.route('/categories/<int:category_id>/items/<int:item_id>/update', \
	methods = ['GET', 'POST'])
@login_required
def updateItem(category_id, item_id):
	""" Update a specific item.

	GET: Display the "update item" page.
	POST: Accept the form from "update item" page,
		  update that specific item accordingly and save it to database.
	"""

	activeCategory = session.query(Category).filter_by(\
		id = category_id, \
		creator_id = current_user.id).first()

	categories = session.query(Category).filter_by(\
		creator_id = current_user.id).all()

	activeItem = session.query(Item).filter_by(\
		id = item_id, \
		creator_id = current_user.id).first()

	if (activeCategory is not None) and (activeItem is not None):
		if request.method == 'GET':
			return render_template('item_update.html', \
				categories = [category.serialize for category in categories], \
				activeCategory = activeCategory, \
				item = activeItem, \
				id = category_id)

		elif request.method == 'POST':
			# receive data from create page form, store it to database
			data = request.form
			name = data.get('iname')
			desc = data.get('idesc')

			if name != '' and name is not None:
				# An item's cannot be blank,
				# But its decription can be.
				activeItem.name = name
				activeItem.description = desc
			
			session.add(activeItem)
			session.commit()

			flash('Item "{}" is updated.'.format(activeItem.name), 'success')

			return redirect(url_for('displayOneCategory', \
				category_id = category_id))

	else:
		abort(404)

@app.route('/categories/<int:category_id>/items/<int:item_id>/delete', \
	methods = ['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
	""" Delete a specific item.

	GET: Display the "delete item" page.
	POST: Accept the form from "delete item" page,
		  delete that specific item accordingly and save it to database.
	"""

	activeCategory = session.query(Category).filter_by(\
		id = category_id, \
		creator_id = current_user.id).first()

	categories = session.query(Category).filter_by(\
		creator_id = current_user.id).all()

	activeItem = session.query(Item).filter_by(\
		id = item_id, \
		creator_id = current_user.id).first()

	if (activeCategory is not None) and (activeItem is not None):
		if request.method == 'GET':
			return render_template('item_delete.html', \
				categories = [category.serialize for category in categories], \
				activeCategory = activeCategory, \
				item = activeItem, \
				id = category_id)

		elif request.method == 'POST':

			delName = activeItem.name

			session.delete(activeItem)
			session.commit()

			flash('Item "{}" is deleted.'.format(delName), 'success')

			return redirect(url_for('displayOneCategory', \
				category_id = category_id))

	else:
		abort(404)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	""" Log user in. 
	For all other pages, except logout page, 
	the user will be redirected here is not logged in.

	GET: Display the login page
	POST: Receives JSON file from the browser, checks it,
	      decode the id_token received using Google's OAuth library,
		  get the id info and decide whether the login is successful or not.
	"""

	if request.method == 'GET':
		login_session['state'] = os.urandom(24).encode('hex')
		return render_template('login.html', \
			state = login_session['state'], \
			CLIENT_ID = CLIENT_ID)

	elif request.method == 'POST':
		# Check Session State
		if request.args.get('state') != login_session['state']:
			return jsonify(error = "Invalid state parameter"), 401
		
		# Process ID Token from Google
		try:
			token = request.data
			idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

			# print idinfo['iss']
			# print idinfo['email']
			# print idinfo['name']
			# print idinfo['sub']
			# print idinfo['aud']

			if idinfo['iss'] not in ['accounts.google.com', \
									 'https://accounts.google.com']:
				# Wrong Issuer
				raise ValueError('The issuer of your ID information is not accepted.')

			if idinfo['aud'] != CLIENT_ID:
				# Wrong Audience
				raise ValueError('We are not the audience of your ID information.')

			user = session.query(User).filter_by(gid = idinfo['sub']).first()

			if not user:
				# User previously did not exist, create one.
				user = User(\
					gid = idinfo['sub'],\
					username = idinfo['name'],\
					email = idinfo['email'],\
					picture = idinfo['picture'],\
					is_authenticated = True,\
					is_active = True, \
					is_anonymous = False)

				session.add(user)
				session.commit()

			login_user(user)

			flash('Login successful. Welcome, {}!'.format(user.username), 'success')

			return "success"

		except Exception, error:
			return jsonify(error = str(error)), 401

@app.route('/logout')
def logout():
	""" Log user out. (Accepts GET requests only) """
	logout_user()
	return render_template('logout.html', CLIENT_ID = CLIENT_ID)

@app.route('/me')
@login_required
def showUser():
	""" Display the current user's profile. """
	return render_template('user.html')

@app.route('/me/json')
@login_required
def jsonUser():
	""" JSON Entry. Return the current user's profile. """
	return jsonify(id = current_user.id,\
		username = current_user.username,\
		email = current_user.email,\
		picture = current_user.picture)

@app.route('/json')
@app.route('/categories/json')
@login_required
def jsonAllCategories():
	""" JSON Entry. Return all categories """
	categories = session.query(Category).filter_by(\
		creator_id = current_user.id).all()

	return jsonify(categories = [category.serialize for category in categories])

@app.route('/categories/<int:category_id>/json')
@login_required
def jsonCategory(category_id):
	""" JSON Entry. Return a specific categories with its items. """
	category = session.query(Category).filter_by(\
		id = category_id, \
		creator_id = current_user.id).first()

	items = session.query(Item).filter_by(\
		category_id = category_id, \
		creator_id = current_user.id).all()

	if category is not None:
		category_with_items = category.serialize
		category_with_items['items'] = [item.serialize for item in items]
		return jsonify(category = category_with_items)

	else:
		return jsonify(error = "Category not found.")

@app.route('/categories/<int:category_id>/items/<int:item_id>/json')
@login_required
def jsonItem(category_id, item_id):
	""" JSON Entry. Return a specific item. """
	item = session.query(Item).filter_by(\
		id = item_id, \
		creator_id = current_user.id).first()

	if item is not None:
		return jsonify(item = item.serialize)

	else:
		return jsonify(error = "Item not found.")

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
def showError(error):
	""" Display error page. """
	return render_template('error.html', error = error), error.code


if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'Secret Key'
	app.run(host='0.0.0.0', port=8000)
