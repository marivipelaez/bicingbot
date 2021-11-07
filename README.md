# BicingBot

Telegram bot that shows the status of your favorite stations of [Bicing](https://www.bicing.cat/), the Barcelona's public bike rental system.

## Installation

### Requirements

* Install Python3: https://www.python.org/ (tested with python 3.9)
### Project dependencies

* Create a new `virtualenv` called `bicingbot` and activate it.

```sh
# If working with virtualenvwrapper
$ mkvirtualenv bicingbot
```

* Install python dependencies: `(bicingbot)$ pip install -r requirements.txt`
* Install python dev dependencies: `(bicingbot)$ pip install -r requirements_dev.txt`

### Build and run
* Activate virtualenv

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

* Run `bicingbot` server:

```sh
$ python bicingbot/bicingbot_app.py
```

Now, open the browser pointing to http://localhost:5000

## Development

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) as HTTP server to publish the `BicingBot API callbacks`.
* [Sqlite3](https://docs.python.org/3/library/sqlite3.html) as database.
* [Telegram python library](https://github.com/python-telegram-bot/python-telegram-bot) to connect to `Telegram`.
* [Bicing API](https://www.bicing.barcelona/get-stations) to get Bicing Stations information
