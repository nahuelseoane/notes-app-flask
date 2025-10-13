from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user
from app.models import User, db
from app.forms.auth_forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists", "error")
            return redirect(url_for("auth.register"))

        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("notes.notes_home"))
        else:
            flash("User not allowed.", "error")
    return render_template("login.html", form=form)


@auth_bp.route("logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))