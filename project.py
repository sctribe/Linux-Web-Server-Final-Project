from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
app = Flask(__name__)

from database_setup import Base, Genre, Songs, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import session as login_session
import random, string, json, httplib2, requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

##Create session and connect to DB
engine = create_engine("sqlite:///musicgenreswithusers.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/")
@app.route("/genres")
def showGenres():
	genres = session.query(Genre).all()
	if "username" not in login_session:
		return render_template("publicGenres.html", genres = genres)
	else:
		loginUser = login_session["user_id"]
		return render_template("genres.html", genres = genres, loginUser = loginUser)


@app.route("/genres/new", methods = ["GET", "POST"])
def newGenre():
	if "username" not in login_session:
		return redirect('/login')
	if request.method == "POST":
		if request.form["name"]:
			newGenre = Genre(name = request.form["name"], user_id = login_session["user_id"])
			session.add(newGenre)
			session.commit()
			return redirect(url_for("showGenres"))
		else:
			return render_template("newGenre.html")
	else:
		return render_template("newGenre.html")


@app.route("/genres/<int:genre_id>/edit/", methods = ["GET", "POST"])
def editGenre(genre_id):
	if "username" not in login_session:
		return redirect("/login")
	editedGenre = session.query(Genre).filter_by(id = genre_id).one()
	if editedGenre.user_id != login_session["user_id"]:
		return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own genre in order to edit.');}</script><body onload='myFunction()''>"
	if request.method == "POST":
		if request.form["name"]:
			editedGenre.name = request.form["name"]
			return redirect(url_for("showGenres"))
	else:
		return render_template("editGenre.html", genre = editedGenre)


@app.route("/genres/<int:genre_id>/delete/", methods = ["GET", "POST"])
def deleteGenre(genre_id):
	if "username" not in login_session:
		return redirect("/login")
	deletedGenre = session.query(Genre).filter_by(id = genre_id).one()
	if deletedGenre.user_id != login_session["user_id"]:
		return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own genre in order to edit.');}</script><body onload='myFunction()''>"
	if request.method == "POST":
		session.delete(deletedGenre)
		session.commit()
		return redirect(url_for("showGenres"))
	else:
		return render_template("deleteGenre.html", genre = deletedGenre)


@app.route("/genre/<int:genre_id>/")
@app.route("/genre/<int:genre_id>/songs/")
def showSongs(genre_id):
	genre = session.query(Genre).filter_by(id = genre_id).one()
	#creator = getUserInfo(genre.user_id)
	songs = session.query(Songs).filter_by(genre_id = genre_id).all()
	if "username" not in login_session:
		return render_template("publicSongs.html", genre = genre, songs = songs)
	else:
		loginUser = login_session["user_id"]
		return render_template("songs.html", genre = genre, songs = songs, loginUser = loginUser)


@app.route("/genre/<int:genre_id>/songs/new", methods = ["GET", "POST"])
def newSong(genre_id):
	if "username" not in login_session:
		return redirect("/login")
	fromGenre = session.query(Genre).filter_by(id = genre_id).one()
	if request.method == "POST":
		newSong = Songs(name = request.form["name"],album = request.form["album"],artist = request.form["artist"],
			year = request.form["year"], length = request.form["length"], genre_id = genre_id, user_id = login_session["user_id"])
		session.add(newSong)
		session.commit()

		return redirect(url_for("showSongs", genre_id = genre_id))

	else:
		return render_template("newSong.html", genre_id = genre_id, genre = fromGenre)


@app.route('/genre/<int:genre_id>/songs/<int:song_id>/edit', methods = ["GET", "POST"])
def editSong(genre_id, song_id):
	if "username" not in login_session:
		return redirect("/login")
	editedSong = session.query(Songs).filter_by(id = song_id).one()
	if editedSong.user_id != login_session["user_id"]:
		return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own genre in order to edit.');}</script><body onload='myFunction()''>"
	if request.method == "POST":
		if request.form["name"]:
			editedSong.name = request.form["name"]
		if request.form["artist"]:
			editedSong.artist = request.form["artist"]
		if request.form["album"]:
			editedSong.album = request.form["album"]
		if request.form["year"]:
			editedSong.year = request.form["year"]
		if request.form["length"]:
			editedSong.length = request.form["length"]
		session.add(editedSong)
		session.commit()

		return redirect(url_for("showSongs", genre_id = genre_id))
	else:
		return render_template("editSong.html", genre_id = genre_id, song_id = song_id, song = editedSong)


@app.route('/genre/<int:genre_id>/songs/<int:song_id>/delete', methods = ["GET", "POST"])
def deleteSong(genre_id, song_id):
	if "username" not in login_session:
		return redirect("/login")
	deletedSong = session.query(Songs).filter_by(id = song_id).one()
	fromGenre = session.query(Genre).filter_by(id = genre_id).one()
	if deletedSong.user_id != login_session["user_id"]:
		return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own genre in order to edit.');}</script><body onload='myFunction()''>"
	if request.method =="POST":
		session.delete(deletedSong)
		session.commit()

		return redirect(url_for("showSongs", genre_id = genre_id))
	else:
		return render_template("deleteSong.html", genre_id = genre_id, song = deletedSong, genre = fromGenre)


@app.route('/genres/JSON')
def genresJSON():
	genres = session.query(Genre).all()
	return jsonify(genres = [r.serialize for r in genres])


@app.route('/genre/<int:genre_id>/songs/JSON')
def genreSongsJSON(genre_id):
	genre = session.query(Genre).filter_by(id = genre_id).one()
	songs = session.query(Songs).filter_by(genre_id = genre.id).all()
	return jsonify(Songs = [i.serialize for i in songs])


@app.route('/genre/<int:genre_id>/songs/<int:song_id>/edit/JSON')
def songJSON(genre_id, song_id):
	song = session.query(Songs).filter_by(id=song_id).one()
	return jsonify(song = song.serialize)


@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in xrange(32))
	login_session['state']=state
	return render_template('login.html', STATE = state)


@app.route('/gconnect', methods = ['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers["Content-Type"] = 'application/json'
		return response

	code = request.data
	try:
		#Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps("Failed to upgrade the authorization code."), 401)
		response.headers["Content-Type"] = 'application/json'
		return response

	#Check that the access token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, "GET")[1])

	#If there was an error in the access token info, abort.
	if result.get("error") is not None:
		response = make_response(json.dumps(result.get("error")), 5005)
		response.headers["Content-Type"] = 'application/json'
		return response

	#Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers["Content-Type"] = 'application/json'
		return response

	#Verift that the access token is valid for this app.
	if result["issued_to"] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's"), 401)
		print "Token's client ID does not match app's."
		response.headers["Content-Type"] = 'application/json'
		return response

	#Check to see if user is already logged in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps("Current user is already logged in."), 200)
		response.headers["Content-Type"] = 'application/json'
		return response

	#Store the access token in the session for later use.
	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id

	#Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session["picture"] = data["picture"]
	login_session["email"] = data["email"]
	login_session["provider"] = "google"

	#check to see if user exist, if it doesn't make a new one
	user_id = getUserId(login_session["email"])
	if not user_id:
		user_id = createUser(login_session)
	login_session["user_id"] = user_id

	output = ""
	output += "<h1>Welcome!</h1>"
	flash("You are logged in as %s" % login_session["username"])

	return output


def gdisconnect():
	#Only disconnect a connected user.
	credentials = login_session.get("credentials")
	if credentials is None:
		response = make_response(json.dumps("Current user is not connected."), 401)
		response.headers["Content-Type"] = "application/json"
		return response

	#Execute HTTP GET request to revoke current token.
	access_token = credentials.access_token
	url = "https://accounts.google.com/o/oauth2/revoke?token=%s" %access_token
	h = httplib2.Http()
	result = h.request(url, "GET")[0]
	#If status is ok reset the user's session.
	if result["status"] == "200":
		del login_session["credentials"]
		del login_session["gplus_id"]
		del login_session["username"]
		del login_session["email"]
		del login_session["picture"]
		del login_session["provider"]

		response = make_response(json.dumps("User has been successfully disconnected."), 200)
		response.headers["Conent-Type"] = "application/json"
		return response
	#If something goes wrong in the disonnect process
	else:
		response = make_response(json.dumps("Failed to revoke token for given user."), 400)
		response.headers["Content-Type"] = "application/json"
		return response


@app.route("/fbconnect", methods = ["POST"])
def fbconnect():
	if request.args.get("state") != login_session["state"]:
		response = make_response(json.dumps("Invalid state parameter."), 401)
		response.headers["Content-Type"] = "application/json"
		return response
	access_token = request.data


	#Exchange client token for long-lived server side token

	app_id = json.loads(open("fb_client_secrets.json", "r").read())["web"]["app_id"]
	app_secret = json.loads(open("fb_client_secrets.json", "r").read())["web"]["app_secret"]
	url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
	h = httplib2.Http()
	result = h.request(url, "GET")[1]


	#Use token to get user info from API
	userinfo_url = "https://graph.facebook.com/v2.8/me"

	#Strip expire tag from access token
	token = result.split("&")[0]

	url = "https://graph.facebook.com/v2.8/me?%s&fields=name,id,email" % token
	h = httplib2.Http()
	result = h.request(url, "GET")[1]


	data = json.loads(result)


	login_session["provider"] = "facebook"
	login_session['username'] = data['name']
	login_session["facebook_id"] = data["id"]
	login_session["email"] = data["email"]



	#Get user picture
	url = 'https://graph.facebook.com/v2.8/me/picture?%s&redirect=0&height=200&width=200' % token
	h = httplib2.Http()
	result = h.request(url, "GET")[1]
	data = json.loads(result)

	login_session["picture"] = data["data"]["url"]

	#check to see if user exist, if it doesn't make a new one
	user_id = getUserId(login_session["email"])
	if not user_id:
		user_id = createUser(login_session)
	login_session["user_id"] = user_id

	output = ""
	output += "<h1>Welcome!</h1>"
	flash("You are logged in as %s" % login_session["username"])

	return output

@app.route("/fbdisconnect")
def fbdisconnect():
	facebook_id = login_session["facebook_id"]
	#the access token must be included for successful logout
	#access_token = login_session["access_token"]
	url = "https://graph.facebook.com/%s/permissions" % facebook_id
	h = httplib2.Http()
	result = h.request(url, "DELETE")[1]
	del login_session["username"]
	del login_session["email"]
	del login_session["picture"]
	del login_session["user_id"]
	del login_session["facebook_id"]
	del login_session["provider"]
	return "You have been logged out"



@app.route("/logout")
def logout():

	if login_session["provider"] == "google":
		gdisconnect()
		return redirect(url_for("showGenres"))
	elif login_session["provider"] == "facebook":
		fbdisconnect()
		return redirect(url_for("showGenres"))
	else:
		return "You were never logged in!"

#Helper Functions

def createUser(login_session):
	newUser = User(name = login_session["username"], email = login_session["email"], picture = login_session["picture"])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session["email"]).one()
	return user.id

def getUserInfo(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	return user

def getUserId(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None



if __name__ == "__main__":
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = "0.0.0.0", port = 5000)