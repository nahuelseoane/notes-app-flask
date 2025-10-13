# 📝 Flask Notes App

A simple notes web app built with **Flask**, **SQLAlchemy**, and **TailwindCSS**.

## 📷 Screenshot
![Notes App Screenshot](https://i.imgur.com/WydPUEE.png)

## Features
- User authentication (login/register/logout)
- Create, edit, and delete notes
- User-specific notes
- SQLite database with Flask-Migrate
- Responsive UI with TailwindCSS
- Unit tests with unittest

## Setup

```bash
git clone https://github.com/nahuelseoane/notes-app-flask.git
cd notes-app-flask
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
```

