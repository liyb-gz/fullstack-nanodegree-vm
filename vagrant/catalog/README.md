# Catalog App - A Udacity Full Stack Nanodegree Project

## What is this?

This is an application that helps you organize your catagories and items. It can be anything: your favorite singers and their songs, topics that interest you and the related books, you name it. Anything that can be organized in the category-item way can be managed by this app.

## What do I need for this app?

To install this app, you need the followings installed:

- [Python 2](https://www.python.org/downloads/release/python-2714/ "Python 2")
- [Flask](http://flask.pocoo.org/)
- [Flask-login](https://flask-login.readthedocs.io/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Googe API Client Libraries for Python](https://developers.google.com/api-client-library/python/)

But if you stick with Udacity's vagrant VM, you already have **Python**, **Flask** and **SQLAlchemy** installed. Please refer to **[Flask-login](https://flask-login.readthedocs.io/en/latest/)** and **[Googe API Client Libraries for Python](https://developers.google.com/api-client-library/python/)**'s website for installation.

## I have everything ready, how do I install it?

When you are ready for the installation, follow the steps below:

1. Get the source file of this app from Github:
	- If you have Git installed on your computer, open a console and run this command: `git clone https://github.com/liyb-gz/fullstack-nanodegree-vm.git`
	- If you don't have Git, download the ZIP file from this Github repository (come on, you can find the "**Download ZIP**" button!) and unzip it.
2. Open the "fullstack-nanodegree-vm" folder, then the "vagrant" folder inside it.
3. If you want to use Udacity's vagrant VM but haven't set it up, follow this [guide](https://www.udacity.com/wiki/ud197/install-vagrant) to set it up.
4. Open the "catalog" folder.

Now you are ready to run the app!

## How to run this app

To run the app, follow the steps below:

1. Run this command in the "catalog" folder: `python models.py`. This command is for creating a SQLite database file on your machine, as the database file is not included in this Github repository.
2. Run this command: `python application.py` to run the app on the local server.
3. If you didn't change the settings, you can visit the app through [http://localhost:8000](http://localhost:8000). 

Enjoy!
