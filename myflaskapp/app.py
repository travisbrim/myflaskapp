# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, got_request_exception
from flask_mail import email_dispatched

import rollbar
import rollbar.contrib.flask

from myflaskapp import commands, user, public
from myflaskapp.extensions import (bcrypt, bootstrap, cache, csrf_protect, db, debug_toolbar, login_manager,
                                   migrate, webpack, mail, moment)
from myflaskapp.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    @app.before_first_request
    def init_rollbar():
        """init rollbar module"""
        if app.config['ENV'] in ('production',) and app.config['ROLLBAR_API']:
            rollbar.init(access_token=app.config['ROLLBAR_API'],
                         environment=app.config['ENV'],
                         root=app.config['APP_DIR'],
                         allow_logging_basic_config=False)

            got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

    def log_email_message(message, app):
        app.logger.debug(message.body)

    if app.config['DEBUG']:
        email_dispatched.connect(log_email_message)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    webpack.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.bp)
    app.register_blueprint(public.views.bp)


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
