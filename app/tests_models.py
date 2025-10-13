import unittest

from app import create_app
from .models import db, Note, User
from werkzeug.security import generate_password_hash

class NoteTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app("app.config.TestConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_note(self):
        with self.app.app_context():
            # Create a user
            user = User(username="testuser", password_hash=generate_password_hash("password"))
            db.session.add(user)
            db.session.commit()

            # Note
            note_db = Note(title="Title", content="Content", user_id=user.id)
            db.session.add(note_db)
            db.session.commit()

            note = Note.query.first()
            self.assertEqual(note.title, "Title")
            self.assertEqual(note.content, "Content")
            self.assertEqual(note.user_id, user.id)
