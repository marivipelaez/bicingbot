# BicingBot

[![Build Status](https://github.com/marivipelaez/bicingbot/workflows/build/badge.svg?branch=master)](https://github.com/marivipelaez/bicingbot/actions?query=branch%3Amaster)
[![Coverage Status](https://coveralls.io/repos/github/marivipelaez/bicingbot/badge.svg?branch=master)](https://coveralls.io/github/marivipelaez/bicingbot?branch=master)


Telegram bot that shows the status of your favorite stations of [Bicing](https://www.bicing.cat/), the Barcelona's public bike rental system.

## Installation

### Requirements

* Install Python3: https://www.python.org/ (tested with python 3.9)
### Project dependencies

* Create a new `virtualenv` called `bicingbot`:

```sh
$ cd VIRTUALENVS_PATH
$ python venv bicingbot
```

```sh
# If working with virtualenvwrapper
$ mkvirtualenv bicingbot
```

* Activate the `virtualenv`

```sh
# In Windows
$ source VIRTUALENVS_PATH/bicingbot/Scripts/activate
```

```sh
# In Mac
$ source VIRTUALENVS_PATH/bicingbot/bin/activate
```

```sh
# If working with virtualenvwrapper
$ workon bicingbot
```

* Install python dependencies: `(bicingbot)$ pip install -r requirements.txt`
* Install python dev dependencies: `(bicingbot)$ pip install -r requirements_dev.txt`

### Build and run


* Run `bicingbot` server:

```sh
$ python bicingbot/bicingbot_app.py
```

Now, open the browser pointing to http://localhost:5000

## Development

* [Flask](https://pypi.org/project/Flask/2.0.2/) as HTTP server to publish the `BicingBot API callbacks`.
* [Sqlite3](https://docs.python.org/3/library/sqlite3.html) as database.
* [Telegram python library](https://github.com/python-telegram-bot/python-telegram-bot) to connect to `Telegram`.
* [Bicing API](https://www.bicing.barcelona/get-stations) to get Bicing Stations information
