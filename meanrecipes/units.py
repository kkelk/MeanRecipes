#!/usr/bin/env python3

'''
This module contains various data tables for converting and normalising units.
'''

# An entry:
#   A: (B, n)
# means convert a value of x in units A to a value of nx in units B
CONVERSIONS = {
    'tablespoons': ('tbsp', 1),
    'tablespoon': ('tbsp', 1),
    'teaspoons': ('tsp', 1),
    'teaspoon': ('tsp', 1),
    'tubs': ('tub', 1),
    'kg': ('g', 1000.0),
    'l': ('ml', 1000.0),
}

ALLOWED_UNITS = (
    'g',
    'tbsp',
    'tsp',
    'tin',
    'punnet',
    'pot',
    'tub',
    'ml'
)



def convert_ingredient(ingredient):
    '''
    This function normalises the representation of certain units, e.g.
    "tablespoons" → "tbsp", to make sure that we can convert them properly.
    There are three normalisations:
        - conversion to lowercase
        - applying rewrite rules as described above, with optional scale
          factors --- this means we can perform unit conversions as well
        - (crude) depluralisation
    '''
    quantity, unit, name = ingredient

    unit = unit.lower()
    previous = ''

    while unit != previous:
        previous = unit
        unit, factor = CONVERSIONS.get(unit, (unit, 1))
        quantity *= factor

    if name.endswith('s'):
        name = name[:-1]

    return (quantity, unit, name)
