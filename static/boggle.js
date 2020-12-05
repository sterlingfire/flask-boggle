"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;

/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(dataBoard) {
  $table.empty();

  // loop over board and create the DOM tr/td structure
  let $tbody = $("<tbody>");

  for (let dataRow of dataBoard) {
    let $tr = $("<tr>");

    for (let dataLetter of dataRow) {
      let $td = $("<td>").text(dataLetter);
      $tr.append($td);
    }

    $tbody.append($tr);
  }

  $table.append($tbody);
}

/** Display message */

function displayMessage(message) {
  $message.text(message)
}


/** Add a valid word to the Word List 
 *  - add a new li item to the .word ul
 */

function displayValidWord(word) {
  
  let $li = $("<li>").text(word);

  $playedWords.append($li);
}


/** Check to see word is valid in the game board.
 *  Sends API request to /api/score-word
 */

async function checkWord(evt) {
  evt.preventDefault();
  $message.empty();


  let word = $wordInput.val().toUpperCase();
  let data = { gameId, word };
  let response = await axios.post("/api/score-word", data);

  // if invalid move, display message
  if (response.data.result !== "ok"){
    let msg = (response.data.result === "not-word")
      ? "That is not a word" : "That word is not in the board";
    
    displayMessage(msg);
  } else {
    // if valid move, add word to playedwords
    displayValidWord(word);
  }

  evt.target.reset();
}

$form.on("submit", checkWord);


start();
