# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from myflaskapp.email import send_password_reset_email
from myflaskapp.extensions import login_manager, db
from myflaskapp.public.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from myflaskapp.user.forms import RegisterForm
from myflaskapp.user.models import User
from myflaskapp.utils import flash_errors

blueprint = Blueprint(name='public',  # pylint: disable=invalid-name
                      import_name=__name__,
                      static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)

    return render_template('public/home.html', nav_form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/login/', methods=['GET', 'POST'])
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
    return render_template('public/login.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', nav_form=form)


@blueprint.route('/reset_password_request/', methods=['GET', 'POST'])
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
        return redirect(url_for('public.login'))
    return render_template('public/reset_password_request.html',
                           title='Reset Password',
                           nav_form=nav_form, form=form)
# FIXME: I shouldnt have to send form and form2
# /register has two forms but somehow manages fine only passing one
# What is different?


@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
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
        return redirect(url_for('public.login'))
    return render_template('public/reset_password.html', form=form)
