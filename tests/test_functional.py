# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import re

from flask import url_for

from myflaskapp.extensions import mail
from myflaskapp.user.models import User
from .factories import UserFactory


class TestLoggingIn:
    """Login."""

    def test_login_return_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_alert_on_logout(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('user.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_error_message_incorrect_password(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert 'Invalid password' in res

    def test_error_message_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown user' in res


class TestRegistering:
    """Register a user."""

    def test_can_register(self, user, testapp):
        """Register a new user."""
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get('/')
        # Clicks Create Account button
        res = res.click('Create account')
        # Fills out the form
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_error_message_passwords_dont_match(self, user, testapp):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = testapp.get(url_for('user.register'))
        # Fills out form, but passwords don't match
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert 'Passwords must match' in res

    def test_error_message_user_already_registered(self, user, testapp):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for('user.register'))
        # Fills out form, but username is already registered
        form = res.forms['registerForm']
        form['username'] = user.username
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert 'Username already registered' in res

    def test_confirm_email_sent(self, db, testapp):
        """Send confirmation email"""
        # Goes to registration page
        with mail.record_messages() as outbox:

            res = testapp.get(url_for('user.register'))

            form = res.forms['registerForm']
            form['username'] = 'pandas'
            form['email'] = 'foo@bar.com'
            form['password'] = 'secret'
            form['confirm'] = 'secret'

            res = form.submit()

            assert len(outbox) == 1
            assert 'Confirm Your Email Address' in outbox[0].subject

    def test_email_confirmation(self, db, testapp):
        """Confirm a user's email address"""
        # Goes to registration page
        with mail.record_messages() as outbox:
            res = testapp.get(url_for('user.register'))

            form = res.forms['registerForm']
            form['username'] = 'pandas'
            form['email'] = 'foo@bar.com'
            form['password'] = 'secret'
            form['confirm'] = 'secret'

            res = form.submit()

            body_html = outbox[0].html

        groups = re.search('<a href=\"http://localhost(.*)\">', body_html)
        confirmation_url = groups[1]

        res = testapp.get(confirmation_url)

        assert User.get_by_id(1).email_confirmed is True
