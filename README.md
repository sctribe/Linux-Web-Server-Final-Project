# Music Catalog Project

The purpose of this project was to develop a catalog web application that provides for a variety of
categories as well as a user registration and authentication system. Users who login with Facebook or Google
Plus can post, edit, and delete their own posts. Logged in users can not modifty posts that don't belong to
them in any way.

## Files/Folders

#### templates

This folder contains all of the html files for the web application

#### static

This folder contains the css file for the web application

#### database_setup.py

This file containts the database scheme. Creates 3 tables titled Users, Genres, and Songs.

#### genre_populator.py

This file contains code necessary to populate the database. This is provided to make it easier
to see how the application functions

#### client_secrets.json/fb_client_secrets.json

These files contain the information necessary to implement Google Plus and Facebook oAuth functionality.

#### project.py

Contains the Flask application. All code tying the sql database and html together is found here.

## How to Run

1. Download Vagrant VM from Udacity
2. Open Terminal and navigate to vagrant folder
  * Type `vagrant up`
3. SSH in to the Vagrant VM by typing `vagrant ssh`
4. Before going any further run the following commands to make sure you have the correct version of Flask
   installed on your VM.
   * Type `sudo pip install werkzeug==0.8.3`
   * Type `sudo pip install flask==0.9`
   * Type `sudo pip install Flask-Login==0.1.3`
5. Type in `cd /vagrant/catalog` to navigate to the project folder
6. Type in `python database_setup.py` to create the database
7. Type in `python genre_populator.py` to populate the database. Note that no users will be able to delete
   the entries created by this script since they are attributed to a sample user
8. Type in `python project.py` to start the server
9. Access and test the application locally by visiting http://localhost:5000 in a web browser

