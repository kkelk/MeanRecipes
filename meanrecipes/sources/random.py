#!/usr/bin/env python3
import random
from recipe import Recipe, RecipeSource

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

