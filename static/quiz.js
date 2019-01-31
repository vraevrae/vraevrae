// vue templating setup en state initialisation
let vue_question = new Vue({
  // element that contains vue template
  el: '#vue_question',
  // data to feed to the template
  data: {
    quiz: {},
    question: {},
    answers: [],
    timer: 0,
    send_answer: send_answer
  }
})

// socket setup
let socket = io.connect('http://' + document.domain + ':' + location.port)

// destructure variables onto the current scope (window) to make them available everywhere
// TODO: make this use of window scope a tad less dirty by enclosing this entire thing in a function
// should still work due to function closures
let { quiz_id, user_id } = document.querySelector('#data').dataset

// if socket connected succesfully
socket.on('connect', function() {
  console.log('[SOCKET_IO]: Socket connected')
  socket.emit('join_game', { quiz_id, user_id })
  get_current_question()
})

// get current question from server
function get_current_question() {
  console.log('[SOCKET_IO]: GET NEW QUESTION')
  socket.emit('get_current_question', { quiz_id, user_id })
}

// if socket receives new question from the server
socket.on('current_question', function(data) {
  console.log('[SOCKET_IO]: CURRENT QUESTION: ', data)

  // write data to the vue state to get reactive templating
  vue_question.answers = data.answers
  vue_question.question = data.question
  vue_question.quiz = data.quiz

  // start the interval because time is known
  setInterval(setTimer, 500)
  setInterval(get_current_question, 10000)
})

// function to send answer to the server
function send_answer(answer_id) {
  console.log('[SOCKET_IO]: SEND ANSWER', answer_id)
  socket.emit('send_answer', { user_id, answer_id, quiz_id })
}

// if server received answer
socket.on('received_answer', function(data) {
  console.log('[SOCKET_IO]: RECEIVED ANSWER SUCCESS', data)

  // remove the question and answers
  vue_question.question.text = 'Waiting for next question'
  vue_question.answers = []
})

function setTimer() {
  // get time from the vue store and get current time
  let start_time = new Date(vue_question.quiz.start_time)
  let curr_time = new Date()

  // TODO: equalise time in the worst possible way (this ain't gonna work in summer)
  curr_time.setHours(curr_time.getHours() - 1)

  // calculate the difference and transform it to a timer
  difference = (curr_time.getTime() - start_time.getTime()) / 1000
  timer = 10 - (difference % 10)

  // write the timer to the vue state
  vue_question.timer = timer

  // TODO: figure out when to trigger socket event, only sets correct time now.
  // Perhaps a parallel interval
}
