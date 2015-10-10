#!/usr/bin/env python3
# average.py
# Contains the logic for actually computing the average recipe.

import functools, warnings
from meanrecipes.recipe import Recipe
from meanrecipes.units import normalise_unit

def ingredient_sum(a, b):
    '''
    Computes the sum of two ingredients, taking into account units. Do note
    that, due to the treatment of name, this sum is not commutative.
    '''
    quantity_a, unit_a, name = a
    quantity_b, unit_b, _ = b

    if unit_a != unit_b:
        warnings.warn('Undefined sum between incompatible units %s and %s' % (unit_a, unit_b))
    
    return (quantity_a + quantity_b, unit_a, name)

def ingredient_scale(a, n):
    '''
    Multiply the ingredient a by the scalar n.
    '''
    quantity, unit, name = a
    return (quantity * n, unit, name)

# The additive identity ingredient.
def ingredient_zero(unit):
    return (0, unit, '')



def normalise_units(intermediates, average):
    '''
    This pass normalises units according to the rules in units.py.
    '''
    for intermediate in intermediates:
        intermediate.ingredients = [(quantity, normalise_unit(unit), name)
                                    for quantity, unit, name in intermediate.ingredients]

    return intermediates, average


def take_mean_of_all_ingredients(intermediates, average):
    '''
    This pass adds every ingredient from the intermediates into the average,
    with a quantity which is the mean of all the individual quantities.
    '''
    totals = dict((r[2], r) for r in average.ingredients)

    # Add up all the ingredient quantities
    for recipe in intermediates:
        for ingredient in recipe.ingredients:
            quantity, unit, name = ingredient
            totals[name] = ingredient_sum(ingredient,
                                          totals.get(name, ingredient_zero(unit)),)

    # And scale them back down to get the mean
    # (dividing by n + 1 since the input working average contributed)
    factor = 1 / (len(intermediates) + 1)
    for name in totals.keys():
        totals[name] = ingredient_scale(totals[name], factor)

    return intermediates, Recipe(average.title,
                                 list(totals.values()),
                                 average.method)



compose = functools.partial(functools.reduce, lambda f, g: lambda *a: g(*f(*a)))

def average(intermediates, working_average):
    # The actual average function is the composition of all the passes, but we
    # ignore the intermediates that are left over.
    the_map = compose([
                normalise_units,
                take_mean_of_all_ingredients
              ])
    _, result = the_map(intermediates, working_average)
    return result
