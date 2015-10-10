#!/usr/bin/env python3
from flask import Flask, url_for, render_template
from sources.random import RandomRecipeSource
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/recipe/search/<term>')
def recipe(term=None):
    source = RandomRecipeSource()
    recipe = next(source.search(term))

    return render_template('recipe.json', title=recipe.title, ingredients=recipe.ingredients, method=recipe.method)

if __name__ == '__main__':
	app.run(debug = True)
