#!/usr/bin/env python3
# average.py
# Contains the logic for actually computing the average recipe.

import functools, warnings
from meanrecipes.recipe import Recipe
from meanrecipes.units import ALLOWED_UNITS, convert_ingredient

def ingredient_sum(a, b):
    '''
    Computes the sum of two ingredients, taking into account units. Do note
    that, due to the treatment of name, this sum is not commutative.
    '''
    quantity_a, unit_a, name = a
    quantity_b, unit_b, _ = b

    if unit_a != unit_b:
        warnings.warn('Attempted sum between incompatible units %s and %s' % (unit_a, unit_b))
        return None
    
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



def convert_units(intermediates, average):
    '''
    This pass normalises units according to the rules in units.py.
    '''
    for intermediate in intermediates:
        intermediate.ingredients = map(convert_ingredient, intermediate.ingredients)

    return intermediates, average


def remove_suspicious_units(intermediates, average):
    '''
    Even once we have the grammatical parsing, we consider some semantic
    questions: what things actually make sense as units? There are surprisingly
    few, certainly versus the cases where names of ingredients masquerade as
    units. So if we come across a unit name that doesn't seem right, presume
    we're dealing with a dimensionless quantity of a thing.
    '''
    for intermediate in intermediates:
        new_ingredients = []

        for quantity, unit, name in intermediate.ingredients:
            if unit not in ALLOWED_UNITS:
                name = (unit + ' ' + name).strip()
                unit  = ''

            new_ingredients.append((quantity, unit, name))

        intermediate.ingredients = new_ingredients

    return intermediates, average


def take_mean_of_all_ingredients(intermediates, average):
    '''
    This pass adds every ingredient from the intermediates into the average,
    with a quantity which is the mean of all the individual quantities.
    '''
    totals = dict((r[2], r) for r in average.ingredients)

    # The factor we scale by to take the mean
    # (dividing by n + 1 since the input working average contributed)
    factor = 1 / (len(intermediates) + 1)

    # Add up all the ingredient quantities
    for recipe in intermediates:
        for ingredient in recipe.ingredients:
            quantity, unit, name = ingredient

            total = ingredient_sum(ingredient,
                                    totals.get(name, ingredient_zero(unit)),)

            if total is None:
                totals[name] = ingredient_scale(ingredient, 1 / factor)
            else:
                totals[name] = total


    # And scale them back down to get the mean
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
                convert_units,
                remove_suspicious_units,
                take_mean_of_all_ingredients
              ])
    _, result = the_map(intermediates, working_average)
    return result
