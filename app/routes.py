from flask import render_template, request, g
import requests

from app import app
from .forms import PokeForm, LoginForm, RegisterForm

@app.route('/')
def index():
	return render_template('index.html')

#Makes a string Look Like This instead-of-like-this
def fmt(string):
	return string.title().replace('-', ' ')

#Yoinks the desired info out of the json from the api
def get_info(data):
	stats = []
	#Grab all the stats and stick them in a list
	for stat in data['stats']:
		stinfo = {}
		stinfo['name'] = fmt(stat['stat']['name'])
		stinfo['level'] = stat['base_stat']
		stats.append(stinfo)
	#Grab the rest of the info and throw everything into a dictionary
	return {
		'abilities': [fmt(ability['ability']['name']) for ability in data['abilities']],
		'exp': data['base_experience'],
		'name': fmt(data['name']),
		'sprite': data['sprites']['front_shiny'],
		'types': [fmt(tp['type']['name']) for tp in data['types']],
		'stats': stats
	}

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
	form = PokeForm()
	#Check if the user has loaded this page by pressing the submit button
	if request.method == 'POST' and form.validate_on_submit():
		#Load the response for the pokemon name given
		name = request.form.get('name')
		response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower().replace(' ', '-')}")
		#Break if broken
		if not response.ok:
			return render_template('pokemon.html', error='Error: Bad request', form=form)
		#Break if broken (again)
		try:
			info = get_info(response.json())
			return render_template('pokemon.html', info=info, form=form)
		except:
			return render_template('pokemon.html', error="Error: Error processing response", form=form)
	return render_template('pokemon.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	return render_template('register.html', form=form)
