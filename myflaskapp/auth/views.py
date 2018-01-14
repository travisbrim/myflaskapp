# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from myflaskapp.email import send_password_reset_email, send_confirm_email
from myflaskapp.extensions import login_manager, db
from myflaskapp.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from myflaskapp.user.forms import RegisterForm
from myflaskapp.user.models import User
from myflaskapp.utils import flash_errors

auth = Blueprint(name='auth',  # pylint: disable=invalid-name
                 import_name=__name__,
                 static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@auth.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User.create(username=form.username.data,
                           email=form.email.data,
                           password=form.password.data,
                           active=False)
        flash('Thank you for registering. Please validate your email '
              'address before logging in.', 'success')
        send_confirm_email(user)
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('auth/register.html', form=form)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """Login user."""
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('auth/login.html', form=form)




@auth.route('/reset_password_request/', methods=['GET', 'POST'])
def reset_password_request():
    nav_form = LoginForm(request.form)
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('public.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password',
                           nav_form=nav_form, form=form)
# FIXME: I shouldnt have to send form and form2
# /register has two forms but somehow manages fine only passing one
# What is different?


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('public.home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('public.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    if current_user.email_confirmed:
        flash('You have already verified your email address.', 'info')
        return redirect(url_for('public.home'))
    user = User.verify_confirmation_token(token)
    if not user:
        return redirect(url_for('public.home'))
    user.confirm_email()
    user.active = True
    db.session.commit()
    flash('Your email has been confirmed.', 'success')
    return redirect(url_for('public.home'))
