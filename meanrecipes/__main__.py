#!/usr/bin/env python3
from flask import Flask, url_for, render_template, make_response
from sources.allrecipes import AllRecipesSource
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/recipe/search/<term>')
def recipe(term=None):
    source = AllRecipesSource()
    recipe = next(source.search(term))

    resp = make_response(render_template('recipe.json', title=recipe.title, ingredients=recipe.ingredients, method=recipe.method))
    resp.mimetype = 'application/json'
    return resp

if __name__ == '__main__':
    app.run(debug = True)
