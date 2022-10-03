## Features
- Integrated with Pipenv for package managing.
- Fast deloyment to heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.

## Installation

> Important: The boiplerplate is made for python 3.9 but you can easily change the `python_version` on the Pipfile.

The following steps are automatically runned withing gitpod, if you are doing a local installation you have to do them manually:

```sh
pipenv shell;
pipenv install;
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```

## How to Start coding?

All your application code should be written inside the `./src/` folder.

- src/main.py (it's where your endpoints should be coded)
- src/models.py (your database tables and serialization logic)
- src/utils.py (some reusable classes and functions)
- src/admin.py (add your models to the admin and manage your data easily)

For a more detailed explanation, look for the tutorial inside the `docs` folder.

## Remember to migrate every time you change your models

You have to migrate and upgrade the migrations for every update you make to your models:
```
$ pipenv run migrate (to make the migrations)
$ pipenv run upgrade  (to update your databse with the migrations)
```

# Manual Installation for Ubuntu & Mac

⚠️ Make sure you have `python 3.6+` and `PostgreSQL`:
```sh
$ pipenv install (to install pip packages)
$ pipenv run migrate (to create the database)
$ pipenv run start (to start the flask webserver)
```
