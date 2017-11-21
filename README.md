My Flask App
================================

A flasky app.

Quickstart
----------

First, set your app's secret key as an environment variable. For
example, add the following to `.bashrc` or `.bash_profile`.

```bash
export MYFLASKAPP_SECRET='something-really-secret'
```

Run the following commands to bootstrap your environment :

    git clone https://github.com/austinmcconnell/myflaskapp
    cd myflaskapp
    pip install -r requirements/dev.txt
    npm install
    npm start  # run the webpack dev server and flask server using concurrently

You will see a pretty welcome screen.

Generate a secret key like this

```python
import secrets
secrets.token_hex(20)
```
Take the token from above and use it for the
Setup an .env file containing the following information

```ini
# Flask
FLASK_APP=autoapp.py
FLASK_DEBUG=1
MYFLASKAPP_SECRET = secret_token_from_above

# Node
NODE_ENV=development
NPM_CONFIG_PRODUCTION=false

# Database
DB_USERNAME=username
DB_PASSWORD=password
DB_HOST=host
DB_NAME=port
```

Once you have installed your DBMS, run the following to create your
app\'s database tables and perform the initial migration :

    flask db init
    flask db migrate
    flask db upgrade

Deployment To Heroku
--------------------

### Install Heroku Toolbelt


	brew install heroku


### Authenticate with `heroku login`
 You only need to do this once.

 	heroku login

### Create Heroku Project

	heroku create My Flask App

Note: you can leave the project name off and just use `heroku create` and you'll get a randomly named app.

### Set Environment Variables

	heroku config:set NODE_ENV=development NPM_CONFIG_PRODUCTION=false

This will tell Heroku to install all devDependencies as well as the dependencies in your package.json file.


	heroku config:set FLASK_APP=autoapp.py FLASK_DEBUG=0

This sets the pertinent Flask env variables on your heroku dyno.

### Use Webpack to Build Static Assets on Deploy

If you intend to use webpack to build your static assets on deploy to Heroku, make sure the following line is added to your package.json file under `scripts`

	    "postinstall": "npm run build"

Example

```js
  "scripts": {
    "build": "NODE_ENV=production webpack --progress --colors -p",
    "start": "concurrently -n \"WEBPACK,FLASK\" -c \"bgBlue.bold,bgMagenta.bold\" \"npm run webpack-dev-server\" \"npm run flask-server\"",
    "webpack-dev-server": "NODE_ENV=debug webpack-dev-server --port 2992 --hot --inline",
    "flask-server": "FLASK_APP=$PWD/autoapp.py FLASK_DEBUG=1 flask run",
    "lint": "eslint \"assets/js/*.js\"",
    "postinstall": "npm run build"
  }
```

### Push code to Heroku

	git push heroku master

### (Optional) Set Up Auto-Deploy From Github
TODO: Fill in instructions.


### Setup Heroku-Postgres Hobby-Dev Database

	heroku addons:create heroku-postgresql:hobby-dev

hobby-dev is a free postgres instance limited to 10,000 rows.

Add-Ons
-------

### Rollbar

Signup for a free account at [Rollbar](https://rollbar.com)

    heroku addons:create rollbar
    heroku addons:open rollbar

Optionally Set up Github integration and Deploy hooks

Shell
-----

To open the interactive shell, run :

    flask shell

By default, you will have access to the flask `app`.

Running Tests
-------------

To run all tests, run :

    flask test

Migrations
----------

Whenever a database migration needs to be made. Run the following
commands :

    flask db migrate

This will generate a new migration script. Then run :

    flask db upgrade

To apply the migration.

For a full migration command reference, run `flask db --help`.

Asset Management
----------------

Files placed inside the `assets` directory and its subdirectories
(excluding `js` and `css`) will be copied by webpack\'s `file-loader`
into the `static/build` directory, with hashes of their contents
appended to their names. For instance, if you have the file
`assets/img/favicon.ico`, this will get copied into something like
`static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico`. You can
then put this line into your header:

    <link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">

to refer to it inside your HTML page. If all of your static files are
managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they should
cache all your assets forever by including the following line in your
`settings.py`:

    SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year
