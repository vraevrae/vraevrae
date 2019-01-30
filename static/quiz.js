// vue setup
let vue_question_app = new Vue({
  el: '#vue_question',
  data: {
    quiz: {},
    question: {},
    answers: [],
    timer: 10,
    send_answer: send_answer
  }
})

// socket setup
let socket = io.connect('http://' + document.domain + ':' + location.port)
let { quiz_id, user_id } = document.querySelector('#data').dataset

// if socket connected succesfully
socket.on('connect', function() {
  console.log('[SOCKET_IO]: Socket connected')
  socket.emit('join_game', { quiz_id, user_id })
  get_current_question()
})

// function to get current question from server
function get_current_question() {
  console.log('[SOCKET_IO]: GET NEW QUESTION')
  socket.emit('get_current_question', { quiz_id, user_id })
}

// if socket receives new question from the server
socket.on('current_question', function(data) {
  console.log('[SOCKET_IO]: CURRENT QUESTION: ', data)
  vue_question_app.answers = data.answers
  vue_question_app.question = data.question
  vue_question_app.quiz = data.quiz
})

// function to send answer to the server
function send_answer(answer_id) {
  console.log('[SOCKET_IO]: SEND ANSWER', answer_id)
  socket.emit('send_answer', { user_id, answer_id, quiz_id })
}

// if server received answer
socket.on('received_answer', function(data) {
  console.log('[SOCKET_IO]: RECEIVED ANSWER SUCCESS', data)
  vue_question_app.question.text = 'Waiting for next question'
  vue_question_app.answers = []
})

setTimer = () => {
  let start_time = new Date(data.quiz.start_time)
  let curr_time = new Date()
  curr_time.setHours(curr_time.getHours() - 1)
  difference = (curr_time.getTime() - start_time.getTime()) / 1000
  vue_question_app.timer = difference % 10
}
