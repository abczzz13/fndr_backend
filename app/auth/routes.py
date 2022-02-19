from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import Users


@bp.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in redirect to home
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    # Create Login form
    form = LoginForm()

    # Processing form submit
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Login credentials")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)

        # Redirecting to the next page after succesful login
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
