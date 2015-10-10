#!/usr/bin/env python3
import random

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



class RandomRecipeSource(RecipeSource):
    '''
    A recipe source which creates random gibberish recipes, for testing
    purposes.
    '''

    maximum_recipes = 10

    def search(self, term):
        # First, gather a set of random words
        chance = 0.001
        with open('/usr/share/dict/words') as wordlist:
            words = [line.strip() for line in wordlist if random.uniform(0, 1) <= chance]

        pick = lambda n: ' '.join(random.choice(words) for i in range(n))

        # Then put them together to make a recipe
        for i in range(random.randrange(self.maximum_recipes)):
            title = pick(4)
            n = random.randint(1, 10)
            ingredients = [(random.uniform(0.1, 1000.0), 'g', pick(1)) for _ in range(n)]
            method = [pick(30) for _ in range(n)]

            yield Recipe(title, ingredients, method)


