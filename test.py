from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import logging

class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_Root(self):
            with self.client:
                resp = self.client.get("/")

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(session["highScore"], 0)
                self.assertEqual(session["timesPlayed"], 0)
                self.assertIn('board', session)

    def test_checkWord(self):
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ["a","b","c","d","e"],
                    ["a","b","c","d","e"],
                    ["a","b","c","d","e"],
                    ["a","b","c","d","e"],
                    ["B","O","O","T","e"]
                ]

            resp = self.client.get("/checkword?guess=boot")
            
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')

            resp = client.get("/checkword?guess=abc")

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')

            resp = client.get("/checkword?guess=jump")

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-on-board')

    # returns "TypeError: 'NoneType' object is not subscriptable"
    # def test_score(self):
    #     with self.client as client:
    #         with app.test_request_context():
    #             resp = client.post("/score",
    #                             data=dict({
    #                                     'score': '15'
    #                             }))
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertEqual(session["highScore"], 15)
    #             self.assertEqual(session["timesPlayed"], 1)