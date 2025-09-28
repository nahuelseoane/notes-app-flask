from flask import Flask, jsonify, redirect, request, render_template, url_for

app = Flask(__name__)


@app.route("/")
def hello():
    role = "No admin"
    notes = ["Note 1", "Note 2", "Note 3"]
    return render_template("home.html", role=role, notes=notes)
    
@app.route("/about")
def about():
    return render_template("about.html", app_name="Notes App")

@app.route("/notes")
def notes():
    notes = [
        {"title":"Buy groceries", "content": "Milk, Eggs, Bread"},
        {"title": "Study Flask", "content": "Practice templates and routes"},
        {"title": "Gym", "content": "Leg Day 🤸‍♀️"},
    ]
    return render_template("notes.html", notes=notes)

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
    note = request.args.get("note", "not foud")
    return render_template("confirmation.html", note=note)

@app.route("/create-note", methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        note = request.form.get("note", "Not found")
        return redirect(
            url_for("confirmation", note=note)
        )
    return render_template("note_form.html")