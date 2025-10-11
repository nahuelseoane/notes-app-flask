from flask import Blueprint, request, redirect, url_for

users_bp = Blueprint("users", __name__)

@users_bp.route("/create-user", methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        pass
    return redirect(
        url_for("home")
    )