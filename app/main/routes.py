from datetime import datetime
from flask import render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user
from app.main import bp
from app.models import Users
from app.auth.forms import LoginForm, EditProfileForm
from app import db


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = EditProfileForm(current_user.username)
    # Processing form submit
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.username.data = current_user.username

    user = Users.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title='User Profile', user=user, form=form)


@bp.route('/upload')
def upload():
    return render_template('upload.html', title='Upload')
