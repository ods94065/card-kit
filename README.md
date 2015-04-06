# Python Card-Kit

This is a simple game framework for developing card games in Python,
using the Pygame library. It has been tested with Python 2.7.

## Installing

Clone the repository, then use `python setup.py install` to install
the library. Alternatively, if you are using `pip` and have `git`, you
can install the latest and greatest by doing this:

    pip install git+https://github.com/ods94065/card-kit.git

To install this application's dependencies (I recommend you have a
virtualenv environment activated before doing this), run:

    pip install -r requirements.txt

## Running tests

Run `python setup.py test` to run all unit tests. Alternatively, you
can use `nose2` with various command-line options for more control
over the test run (see [Nose2
documentation](https://nose2.readthedocs.org/en/latest/usage.html) for
details).

## Running demo games

Run `python -m cardkit.simple_game` to see the most basic demo: a bit of
centered text on a widnow.

Run `python -m cardkit.card_game` to see a basic card game: just drawing and
discarding cards.

## License and Credits

Copyright (C) 2015 Owen D. Smith. This software is released under the
GNU Lesser General Public License 3.0; see LICENSE for details.

The source for the card artwork comes from
[vectorized-playing-cards](https://code.google.com/p/vectorized-playing-cards/),
which is also released under the GNU Lesser General Public License
3.0. I rasterized the deck and added a joker card on 5-Apr-2015; only
the rasterized version is currently used here.
