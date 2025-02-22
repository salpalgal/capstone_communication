import os
from unittest import TestCase
from flask import g, session
from models import db, connect_db, User
from api_key import email, app_password

os.environ['DATABASE_URL'] = "postgresql:///communication_db"

from app import app, CURR_USER_KEY


app.config['WTF_CSRF_ENABLED'] = False


class SendEmailTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""

        
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email=email,
                                    password="testuser",
                                    image_url=None,
                                    first_name="Bob",
                                    last_name="Builder")
                                    
        self.testuser_id = 1001
        self.testuser.id = self.testuser_id

        db.session.commit()
       
        

    def test_login(self):
        with self.client as client:
            res = client.post("/login", data= {"username" :"testuser", "password":"testuser"}, follow_redirects= True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Welcome Bob!" , html)

    def test_logout(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY]= self.testuser.id
            res = client.get("/logout", follow_redirects = True)
            html = res.get_data(as_text = True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn("Communication App", html)
    def send_email(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            res = client.post("/user/1001/email", data ={"password":app_password,"subject" : "testing", "content":"hellow world"}, follow_redirects=True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Bob Builder", html)

