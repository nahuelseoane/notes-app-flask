from flask import redirect, url_for, render_template, request, Blueprint, flash
from flask_login import login_required, current_user
from app.models import Note, db

notes_bp = Blueprint("notes", __name__, template_folder="templates")

@notes_bp.route("/")
@login_required
def notes_home():
    print("Current user:", current_user)
    print("Is authenticated:", current_user.is_authenticated)
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
    return render_template("home.html", notes=notes)


@notes_bp.route("/create-note", methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get("title", "Not found")
        content = request.form.get("content", "Not found")

        note_db = Note(
            title=title, content=content, user_id=current_user.id
        )

        db.session.add(note_db)
        db.session.commit()
        flash("Note created", "success")
        return redirect(url_for("notes.notes_home"))
    return render_template("note_form.html")


@notes_bp.route('/edit-note/<int:id>', methods=["GET", "POST"])
@login_required
def edit_note(id):
    note= Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash("You don't have permission to edit this note.", "error")
        return redirect(url_for("notes.notes_home"))
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        note.title = title
        note.content = content
        db.session.commit()
        flash("Note updated", "success")
        return redirect(url_for("notes.notes_home"))

    return render_template("edit_note.html", note=note)

@notes_bp.route('/delete-note/<int:id>', methods=["GET", "POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash("You don't have permission to edit this note.", "error")
        return redirect(url_for("notes.notes_home"))
    db.session.delete(note)
    db.session.commit()
    return redirect(
        url_for("notes.notes_home")
    )
