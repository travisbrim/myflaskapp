from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user

from myflaskapp.auth.forms import LoginForm
from myflaskapp.utils import flash_errors

public = Blueprint(name='public',  # pylint: disable=invalid-name
                   import_name=__name__,
                   static_folder='../static')


@public.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', nav_form=form)


@public.route('/', methods=['GET', 'POST'])
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
