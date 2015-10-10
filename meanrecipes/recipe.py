#!/usr/bin/env python3

class Recipe:
    '''
    Represents an individual recipe, made up of the following attributes:

      * title
        A string containing a human-readable title or name for the recipe.

      * ingredients
        An iterable of tuples (quantity, unit, name) describing the ingredients
        used in the recipe. Here, quantity is a float representing the amount
        of the ingredient used when the recipe is adjusted to serve one person.
        The values 'unit' and 'name' are strings.

      * method
        A list of strings describing the steps in the recipe.

    '''

    def __init__(self, title, ingredients, method):
        self.title = title
        self.ingredients = ingredients
        self.method = method

    def __repr__(self):
        return '<Recipe "%s">' % self.title


class RecipeSource:
    '''
    Represents a source of raw recipes, e.g. a particular recipe website.
    '''

    def search(self, term):
        '''
        Search the given source for recipes with the given keyword, returning
        an iterator over resulting Recipe objects.
        '''
        raise NotImplemented()



