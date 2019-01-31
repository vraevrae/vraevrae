# vraevrae

A trivia site for the course "webprogrammeren en databases" given by on the University of Amsterdam.

## instalation

To run in development mode:

```
pip install -r requirements.txt
flask run
```

To test the project:

```
pytest
```

The project has about 30 tests, which test the models, api and basic webrequests (socketio code is not tested yet)

To deploy the project:

```
todo
```

## authors

- Rachel ...
- Yunis Demir
- Deniz ...
- Robert-Jan Korteschiel

## notable dependencies

### clientside

- Bootstrap - basic styling
- Socket.io - clientside fast omnidirectional communication
- Vue.js - for reactive clientside templating

### serverside (see requirements.txt)

- Flask-SocketIO - serverside fast omnidirectional communication

### API

- OpenTDB - A trivia database
