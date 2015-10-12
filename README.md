MeanRecipes
===========
The absolutely average recipe generator.

Ever wanted to cook something new, but found that, shockingly, there was more than one recipe published online? Frustrated at having to limit yourself to one arbitrary choice from amongst them? Well, no longer! With *MeanRecipes*, you can enter a recipe search term, we'll search the web for the most similar recipes, and average them all together. **Disclaimer: We can't be held responsible for the negative consequences of actually attempting to follow the produced recipes. If anybody tries, though, do [let us know](mailto:kieran@kierankelk.co.uk).**

This was produced in less than 12 hours for LocalHackDay 2015, in St Andrews University, UK. The code, therefore, is fairly horrible, and there are several bugs (although the documentation isn't all that terrible, and we have a [beautifully documented RESTful API](docs/api.tex) with a single endpoint). It turns out, though, that searching user-submitted recipes online can give you some helpful life advice: for example, *MeanRecipes* can give you a detailed ingredient list and methodology for the production of love.

A "silliness" slider is included which, in vague terms, controls the number of recipes an ingredient must be included in for it to appear in the averaged output. This is useful to reduce the occurrence of tiny portions of a huge number of ingredients, as well as to reduce the effect of recipes that didn't match the search term very well. Setting this to zero should always result in getting a blank recipe, whilst 100 will give every ingredient mentioned on any matching recipe.

In the current version, the only website searched for recipes is [allrecipes](allrecipes.co.uk), but a framework exists to expand this easily to other sources (an example, random source which was used for testing is included).

Usage Instructions
==================
*MeanRecipes* runs on Python 3, and has been specifically tested on Python 3.4.1, but other 3.x versions should work. You will need the ability to install additional Python packages on your system, which will normally require either root privileges or running in a virtual environment.

For convenience, if you are running in Computer Science in St Andrews, a bash script has been provided to generate a convenient virtual environment in your school home directory, and to default to the correct Python version. To use this, simply clone the directory and execute the `setup` script (`./setup`). Otherwise, simply run `python setup.py install`. You might also want to add `python setup.py develop`.

Once the appropriate packages are installed, it should be possible to start the server by simply executing `python meanrecipes` from within the project root directory. Following this, pointing a browser at [localhost:5000](http://localhost:5000) should work.

Known Issues
============
* Portion sizes are not taken into consideration &mdash; if a found recipe produces more, then its ingredients will be more heavily weighted in the output than they should be.
* The produced portion size is not calculated or displayed. We originally intended this to be adjustable, so that any recipe could be scaled to any number of people.
* Plurals are naïvely assumed to always simply be appending an 's'. As a result, ingredients lists have been noted to include elements such as "strawberrie" and even "asparagu".
* Our parser is fairly simple, and often messes up when splitting quantities, units and the ingredient description.
* Only a small, hard-coded list of quantity conversions are supported &mdash; we're likely to deal poorly with recipes that use units we haven't explicitly considered.
* Unicode fractions in ingredient quantities are only sometimes dealt with correctly.
* The produced methods aren't averaged particularly well like the ingredients are. We don't particularly know what it means to average natural language like that, but it sounds fun to try sometime.
* No indicator is given while the request is being processed (which is pretty slow). The server might have died, or the recipe could just have a lot of results.
* General hackathon-quality code, and a number of random crashes, display glitches and empty recipes.
