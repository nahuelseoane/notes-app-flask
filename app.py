import os
from datetime import datetime, timezone
from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)


DB_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "notes.sqlite"
)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"


@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)
    
@app.route("/about")
def about():
    return render_template("about.html", app_name="Notes App")


@app.route("/contact", methods=['get', 'post'])    
def contact():
    if request.method == 'GET':
        return render_template("contact.html")
    if request.method == 'POST':
        return "Form sent correctly", 201
    return "Contact page"

@app.route("/api/info")
def api_info():
    data = { 
        "name": "Notes App",
        "version": "1.1.1",
    }
    return jsonify(data), 200


@app.route("/confirmation")
def confirmation():
    note_id = request.args.get("note_id", type=int)
    action = request.args.get("action", "saved")

    note = Note.query.get_or_404(note_id)
    return render_template("confirmation.html", note=note, action=action)


@app.route("/create-note", methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form.get("title", "Not found")
        content = request.form.get("content", "Not found")

        note_db = Note(
            title=title, content=content
        )

        db.session.add(note_db)
        db.session.commit()

        return redirect(
            url_for("confirmation", note_id=note_db.id, action="created")
        )
    return render_template("note_form.html")


@app.route('/edit-note/<int:id>', methods=["GET", "POST"])
def edit_note(id):
    note= Note.query.get_or_404(id)
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        note.title = title
        note.content = content
        db.session.commit()
        return redirect(
            url_for("confirmation", note_id=note.id, action="updated")
        )

    return render_template("edit_note.html", note=note)

@app.route('/delete-note/<int:id>', methods=["GET", "POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(
        url_for("home")
    )
