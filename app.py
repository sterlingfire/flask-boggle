from flask import Flask, request, render_template, jsonify, session, json
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.route("/api/score-word", methods=["POST"])
def score_word():
    """ Checks if the word is legal then returns a JSON repsonse

        A word is legal if:
        - Is in the wordlist
        - Findable in the board

        Valid responses:
        If not a word:   {result: "not-word"}
        If not on board: {result: "not-on-board"}
        If a valid word: {result: "ok"}

    """

    game_info = request.json

    game_id = game_info["gameId"]
    word = game_info["word"]

    # Our BoggleGame instance
    game = games.get(game_id)

    result = ""
    score = 0
    is_dupe = not game.is_word_not_a_dup(word)
    is_word = game.is_word_in_word_list(word)
    is_on_board = game.check_word_on_board(word)

    if is_word and is_on_board:
        result = "ok"
        score = game.play_and_score_word(word)
    elif not is_word:
        result = "not-word"
    elif not is_on_board:
        result = "not-on-board"

    return jsonify({"score": score, "result": result, "dupe": is_dupe})
