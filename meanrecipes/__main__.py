#!/usr/bin/env python3
from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/recipe/search/<term>')
def recipe(term=None):
    ingredients = [[300.0, 'g', 'flour'], [400.5, 'kg', 'chocolate']]
    method = ['Step 1', 'Step 2']

    return render_template('recipe.json', title=term, ingredients=ingredients, method=method)

if __name__ == '__main__':
	app.run(debug = True)
