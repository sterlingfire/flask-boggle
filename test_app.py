from unittest import TestCase
from flask import json, jsonify

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            # test that you're getting a template
            self.assertIn("""id=\"newWordForm\"""", html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:

            game_data = client.get("/api/new-game").get_data(as_text=True)
            game_data = json.loads(game_data)

            # print("client.get(\"/api/new-game\"):", json)

            # Check the keys in the dictionary
            self.assertIn("gameId", game_data)
            self.assertIn("board", game_data)

            # Check that the board is a list of lists
            self.assertIsInstance(game_data["board"], list)
            self.assertIsInstance(game_data["board"][0], list)

            # Check that new game is stored in the games dictionary
            self.assertIn(game_data["gameId"], games)

    def test_api_score_word(self):
        """ Checks if the word is legal then returns a JSON repsonse

            A word is legal if:
            - Is in the wordlist
            - Findable in the board

            Valid responses:
            If not a word:   {result: "not-word"}
            If not on board: {result: "not-on-board"}
            If a valid word: {result: "ok"}
        """

        with self.client as client:

            game_data = client.get("/api/new-game").get_data(as_text=True)
            game_data = json.loads(game_data)

            game_id = game_data["gameId"]

            game = games[game_id]

            game.board = [
                ['E', 'O', 'B', 'I', 'M'],
                ['A', 'N', 'V', 'A', 'I'],
                ['A', 'I', 'R', 'S', 'Z'],
                ['X', 'B', 'A', 'N', 'D'],
                ['E', 'L', 'B', 'E', 'E']
            ]

            word_data = {"gameId": game_id, "word": "NEED"}
            result = client.post("api/score-word", json=word_data).get_json()
            self.assertEqual(result.get("result"), "ok")

            word_data = {"gameId": game_id, "word": "POTATO"}
            result2 = client.post("api/score-word", json=word_data).get_json()
            self.assertEqual(result2.get("result"), "not-on-board")

            word_data = {"gameId": game_id, "word": "FLARGHEN"}
            result3 = client.post("api/score-word", json=word_data).get_json()
            self.assertEqual(result3.get("result"), "not-word")
