#!/usr/bin/env python3
import re, unicodedata, warnings

class Recipe:
    '''
    Represents an individual recipe, made up of the following attributes:

      * title
        A string containing a human-readable title or name for the recipe.

      * ingredients
        An iterable of tuples (quantity, unit, name) describing the ingredients
        used in the recipe. Here, quantity is a float representing the amount
        of the ingredient used when the recipe is adjusted to serve one person,
        or None if no particular quantity is specified.  The values 'unit' and
        'name' are strings.

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


def parse_number(text):
    '''
    Parses integers and rational numbers into floats from a string containing
    them either whole, expressed as:
        - a Unicode combined fraction character
        - a fraction of the form A '/' B
        - a decimal expansion
    '''

    # Get rid of bothersome Unicode characters
    # (On the LHS of the replace, we have a U+2044 FRACTION SLASH)
    text = unicodedata.normalize('NFKC', text).replace('⁄', '/')

    if '/' in text:
        numerator, denominator = text.split('/')
        return float(numerator) / float(denominator)
    else:
        return float(text)

def parse_ingredient(text):
    '''
    Attempts to parse a human-readable description of an ingredient, e.g.
        250g butter
    into a 3-tuple (quantity, unit, name).

    We expect to find things approximating the following 'grammar':
        <ingredient> ::= (<quantity> <whitespace>* <unit>)? <whitespace>* <name>
        <quantity> ::= {0, 1, ..., 9, ., /} \cup (Unicode fraction characters)
        <unit> ::= [a-zA-Z]+
        <name> ::= .*

    Basically, everything ends up in name if we can't find a quantity.
    '''

    # Before we parse, remove extraneous things in brackets
    text = re.sub('(\\([^)]*\\))', '', text)

    i = 0
    quantity_token = ''
    unit_token = ''

    # Read in any numerical prefix
    is_numeric = lambda c: c.isdigit() or unicodedata.category(c) == 'No'
    while i < len(text) and (is_numeric(text[i]) or text[i] in './'):
        quantity_token += text[i]
        i += 1

    # Skip spaces...
    while i < len(text) and text[i].isspace():
        i += 1

    # If we have a quantity, we might have a unit
    if len(quantity_token) > 0:
        while i < len(text) and not text[i].isspace():
            unit_token += text[i]
            i += 1

    # Skip spaces...
    while i < len(text) and text[i].isspace():
        i += 1

    # And keep the rest as the name
    name = text[i:]

    # Now recover the rest of the fields:
    unit = unit_token

    # Parse the quantity as a number
    try:
        quantity = parse_number(quantity_token)
    except ValueError:
        # This also handles, perhaps unwisely, the case where quantity_token is empty
        warnings.warn('Failed to parse a quantity as a number: %s' % quantity_token)
        quantity = None
        unit = ''


    return (quantity, unit, name)
