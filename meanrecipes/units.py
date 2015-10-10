#!/usr/bin/env python3

'''
This module contains various data tables for converting and normalising units.
'''

NORMALISATIONS = {
    'tablespoons': 'tbsp',
    'tablespoon': 'tbsp',
    'teaspoons': 'tsp',
    'teaspoon': 'tsp',
    'tubs': 'tub',
}

ALLOWABLE_UNITS = (
    'g',
    'tbsp',
    'tsp',
    'tin',
    'punnet',
    'ml',
    'l'
)



def normalise_unit(name):
    '''
    This function normalises the representation of certain units, e.g.
    "tablespoons" → "tbsp", to make sure that we can convert them properly.
    There are three normalisations:
        - conversion to lowercase
        - applying rewrite rules as described above
        - (crude) depluralisation
    '''
    name = name.lower()
    previous = ''

    while name != previous:
        previous = name
        name = NORMALISATIONS.get(name, name)

    if name[-1] == 's':
        name = name[:-1]

    return name
