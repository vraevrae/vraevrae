# Vraevrae

A trivia site for the course "webprogrammeren en databases" given by the University of Amsterdam.

## Description
Aim of our webapplication is to allow users to play trivia quiz against each other. By using our website, the players will be able to expand their miscellaneous knowledge while playing live against other users.

## Installation

To install the project locally, run:
```
pip install -r requirements.txt
```
If you want to run the program in development mode run: 
```
flask run
```
The project has 35 tests, which test the models, api and basic webrequests and socket-io events.
To test the project run:
```
pytest
```

## Usage
Once the user is on the index page, he or she can create a new game or join an already existing game. When creating a new game, the user has to fill in a username and is able to pick a difficulty and a category. For joining an existing game, the user also has to fill in a gamecode. Users who has created the game and other user who have joined the existing game using the game code are placed in a lobby. The game creator is then able to start the game. During the game, users have 10 seconds to answer the question. Chose answers are saved whereby the user are not allowed to change their choices afterward. A new qeustion is retrieved every 10 seconds. Quiz consists of 10 questions in total. After finishing the quiz, the users are redirected to the scoreboard, where they are able to see their scores and which questions they have answered correctly.
Demonstration: https://www.youtube.com/watch?v=qYy6DwczCVI

## Credits
- Yunus Demir
- Robert-Jan Korteschiel
- Deniz Seyfeli
- Rachel de Haan


## Notable dependencies

### Clientside

- Bootstrap - basic styling
- Socket.io - clientside fast omnidirectional communication
- Vue.js - for reactive clientside templating

### Serverside (see requirements.txt)

- Flask-SocketIO - serverside fast omnidirectional communication

### API

- OpenTDB - A trivia database

## Licensing

Copyright (c)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
