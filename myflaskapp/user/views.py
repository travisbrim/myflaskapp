# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint(name='user',  # pylint: disable=invalid-name
                      import_name=__name__,
                      url_prefix='/users',
                      static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')
