var vue_question_app = new Vue({
  el: '#vue_question',
  data: {
    question: {},
    answers: [],
    send_answer: send_answer
  }
})

// create socket connection with server
let socket, user_id, quiz_id, progress_timer

// create interval, so the progressbar can be updated every second
socket = io.connect('http://' + document.domain + ':' + location.port)

// get data from the html file
quiz_id = get_data('quiz_id')
user_id = get_data('user_id')

// if socket connected succesfully
socket.on('connect', function() {
  console.log('Socket connected')
  console.log('quiz_id ->', quiz_id)

  // join game with current quiz_id
  socket.emit('join_game', { quiz_id: quiz_id, user_id: user_id }) // COMMENTED BECAUSE LOBBY
  // ALREADY ADDS
  // TO QUIZ
  get_current_question(quiz_id, user_id)
})

// if socket receives a message from the server
socket.on('message', function(message) {
  console.log('SOCKET MESSAGE: ', message)
})

// if socket receives new question from the server
socket.on('current_question', function(data) {
  vue_question_app.answers = data.answers
  vue_question_app.question = data.question
  console.log('CURRENT QUESTION: ', data)
})

// if server received answer
socket.on('received_answer', function(data) {
  vue_question_app.question = 'Waiting for next question'
  vue_question_app.answers = []
  console.log('RECEIVED ANSWER SUCCESS', data)
})

// function to replace document.getElementById() (so code is better readable)
function get_el(id) {
  return document.getElementById(id)
}

// function to replace document.getElementById().dataset (so code is better readable)
function get_data(name) {
  return get_el('data').dataset[name]
}

// function to update timer every second
function update_timer() {
  console.log('update_timer')
  // get current progress
  let current_progress = get_el('progress_bar').value

  // update current_progress
  current_progress -= 10

  // set new progress
  get_el('progress_bar').value = current_progress

  if (current_progress === 0) {
    console.log('PROGRESS === 0, NEW QUESTION')
    get_current_question()
  }

  return true
}

// function to get current question from server
function get_current_question(
  quiz_id = get_data('quiz_id'),
  user_id = get_data('user_id')
) {
  console.log('GET NEW QUESTION (quiz_id, user_id)', quiz_id, user_id)
  socket.emit('get_current_question', { quiz_id: quiz_id, user_id: user_id })
}

// function to send answer to the server
function send_answer(answer_id) {
  let user_id = get_data('user_id')
  let quiz_id = get_data('quiz_id')

  console.log('SEND ANSWER', answer_id)

  // if the button is clicked, send answer via socket to the server
  socket.emit('send_answer', {
    user_id: user_id,
    answer_id: answer_id,
    quiz_id: quiz_id
  })
}
