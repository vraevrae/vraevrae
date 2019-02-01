# Vraevrae

A trivia site for the course "webprogrammeren en databases" given by the University of Amsterdam.

## Installation

To run in development mode:

```
pip install -r requirements.txt
flask run
```

To test the project:

```
pytest
```

The project has 35 tests, which test the models, api and basic webrequests and socket-io events

To deploy the project:

```
todo
```

## Authors

- Rachel ...
- Yunis Demir
- Deniz ...
- Robert-Jan Korteschiel

## Notable dependencies

### Clientside

- Bootstrap - basic styling
- Socket.io - clientside fast omnidirectional communication
- Vue.js - for reactive clientside templating

### Serverside (see requirements.txt)

- Flask-SocketIO - serverside fast omnidirectional communication

### API

- OpenTDB - A trivia database
