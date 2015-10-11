#!/usr/bin/env python3
# average.py
# Contains the logic for actually computing the average recipe.

import functools, warnings
from meanrecipes.recipe import Recipe
from meanrecipes.units import ALLOWED_UNITS, convert_ingredient

def ingredient_sum(a, b, **kw):
    '''
    Computes the sum of two ingredients, taking into account units. Do note
    that, due to the treatment of name, this sum is not commutative.
    '''
    quantity_a, unit_a, name = a
    quantity_b, unit_b, _ = b

    if unit_a != unit_b or quantity_a is None or quantity_b is None:
        warnings.warn('Attempted sum between incompatible units %s and %s' % (unit_a, unit_b))
        return None
    
    return (quantity_a + quantity_b, unit_a, name)

def ingredient_scale(a, n, **kw):
    '''
    Multiply the ingredient a by the scalar n.
    '''
    quantity, unit, name = a
    return (quantity * n if quantity is not None else quantity, unit, name)

# The additive identity ingredient.
def ingredient_zero(unit):
    return (0, unit, '')



def convert_units(intermediates, average, **kw):
    '''
    This pass normalises units according to the rules in units.py.
    '''
    for intermediate in intermediates:
        intermediate.ingredients = map(convert_ingredient, intermediate.ingredients)

    return intermediates, average


def remove_suspicious_units(intermediates, average, **kw):
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


def take_mean_of_all_ingredients(intermediates, average, **kw):
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


def union_methods(intermediates, average, **kw):
    '''
    This pass is the stupidest possible way of combining methods: we just
    concatenate all the step 1s, then the step 2s, ..., the step ns.
    '''

    new_method = []
    i = 0
    
    while True:
        steps = [r.method[i] for r in intermediates if i < len(r.method)]
        if len(steps) == 0:
            break

        new_method += steps
        i += 1

    return intermediates, Recipe(average.title,
                                 average.ingredients,
                                 new_method)


def cull_similar_methods(intermediates, average, threshold = 0.05, **kw):
    '''
    This pass removes adjacent method steps that are very similar to each
    other, to avoid repetitiveness.

    Here, we define a measure of similarity between two steps, considered as
    sets of words A and B, by
        d(A, B) = \frac{ |A \cap B| }{ \max(|A|, |B|) }.
    
    If the similarity is above a certain threshold, we discard one of them.
    '''
    new_method = []

    for i in range(0, len(average.method) - 1):
        m = min(len(average.method[i]), len(average.method[i + 1]))
        A = set(average.method[i].split(' ')[:m])
        B = set(average.method[i + 1].split(' ')[:m])
        d = len(A.intersection(B)) / m

        if d < threshold:
            new_method.append(average.method[i])

    return intermediates, Recipe(average.title, average.ingredients, new_method)


def cull_rare_ingredients(intermediates, average, silliness = 0, **kw):
    new_ingredients = []
    removed_ingredients = []
    new_method = []

    for ingredient in average.ingredients:
        _, _, ingredient_name = ingredient
        hits = 0

        for intermediate in intermediates:
            for _, _, intermediate_name in intermediate.ingredients:
                if intermediate_name == ingredient_name:
                    hits += 1
                    break

        consensus = hits / len(intermediates)
        if consensus <= silliness:
            new_ingredients.append(ingredient)
        else:
            removed_ingredients.append(ingredient)

    for step in average.method:
        have_seen_banned = False
        for _, _, name in removed_ingredients:
            if name not in step:
                have_seen_banned = True
                break

        for _, _, name in new_ingredients:
            if name in step:
                have_seen_banned = False
                break

        if not have_seen_banned:
            new_method.append(step)

    return intermediates, Recipe(average.title, new_ingredients, new_method)


def average(intermediates, working_average, **kw):
    # The actual average function is the composition of all the passes, but we
    # ignore the intermediates that are left over.
    compose = functools.partial(functools.reduce, lambda f, g: lambda *a, **kw: g(*f(*a, **kw), **kw))
    the_map = compose([
                convert_units,
                remove_suspicious_units,
                take_mean_of_all_ingredients,
                union_methods,
                cull_similar_methods,
                cull_rare_ingredients,
              ])
    _, result = the_map(intermediates, working_average, **kw)
    return result
