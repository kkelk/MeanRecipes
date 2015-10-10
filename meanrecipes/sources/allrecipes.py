#!/usr/bin/env python3

'''
This module scrapes search results and recipes from AllRecipes
(allrecipes.co.uk), a site which collects user-submitted recipes.
'''

import requests
from bs4 import BeautifulSoup
from meanrecipes.recipe import Recipe, RecipeSource, parse_ingredient

class AllRecipesSource(RecipeSource):
    SEARCH_URL = 'http://allrecipes.co.uk/recipes/searchresults.aspx?text=%s'

    def _site_search(self, term):
        '''
        Search the AllRecipes site for recipes matching a given search term,
        returning an iterator over URLs containing the full recipe content.
        '''
        response = requests.get(self.SEARCH_URL % term)
        document = BeautifulSoup(response.text, 'html.parser')

        # Conveniently enough, every result is contained within a <div> with the
        # 'recipe' class.
        for container in document.find_all('div', class_ = 'recipe'):
            # the name is in an <a> with itemprop="name", which also gives the
            # URL
            link_matches = container.find_all('a', itemprop = 'name')

            if len(link_matches) > 0:
                link = link_matches[0]
                yield link['href']
        
    def _fetch_recipe(self, url):
        '''
        Fetch a recipe's content from its URL, as a Recipe object.
        '''
        response = requests.get(url)
        document = BeautifulSoup(response.text, 'html.parser')

        # First, extract the title
        title_container = document.select('section.recipeSummary > h1 > span')
        title = title_container[0].string.strip()

        # Then, find and parse the ingredients
        ingredient_items = document.select('section.recipeIngredients > ul > li > span')
        ingredients = []
        for ingredient_item in ingredient_items:
            text = ingredient_item.string.strip()
            ingredients.append(parse_ingredient(text))

        # Finally, take in the steps in the method and return
        method_items = document.select('section.recipeDirections > ol > li > span')
        method = [item.string.strip() for item in method_items]

        return Recipe(title, ingredients, method)


    def search(self, term):
        # We just plug the two methods above together
        return map(self._fetch_recipe, self._site_search(term))
        
