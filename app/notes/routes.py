from flask import redirect, url_for, render_template, request, Blueprint, flash
from app.models import Note, db

notes_bp = Blueprint("notes", __name__, template_folder="templates")

@notes_bp.route("/")
def notes_home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)
    

# @notes_bp.route("/confirmation")
# def confirmation():
#     note_id = request.args.get("note_id", type=int)
#     action = request.args.get("action", "saved")

#     note = Note.query.get_or_404(note_id)
#     return render_template("confirmation.html", note=note, action=action)


@notes_bp.route("/create-note", methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form.get("title", "Not found")
        content = request.form.get("content", "Not found")

        note_db = Note(
            title=title, content=content
        )

        db.session.add(note_db)
        db.session.commit()
        flash("Note created", "success")
        return redirect(url_for("notes.notes_home"))
        # return redirect(
        #     url_for("notes.confirmation", note_id=note_db.id, action="created")
        # )
    return render_template("note_form.html")


@notes_bp.route('/edit-note/<int:id>', methods=["GET", "POST"])
def edit_note(id):
    note= Note.query.get_or_404(id)
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
    db.session.delete(note)
    db.session.commit()
    return redirect(
        url_for("notes.notes_home")
    )
