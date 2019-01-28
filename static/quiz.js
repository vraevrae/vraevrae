const socket = io.connect('http://' + document.domain + ':' + location.port);

$(document).ready(function() {
  let quiz_id = document.getElementById("data").dataset.quiz_id;
  let user_id = document.getElementById("data").dataset.user_id;

  let current_progress = 100;

  let interval = setInterval(function () {
    current_progress -= 10;
    $('#quiz-progress')
        .css('width', `${current_progress}%`)
        .attr('aria-valuenow', current_progress);

    // if (current_progress === 0) {
    //     location.reload();
    //     clearInterval(interval)
    // }
  }, 1000);

  socket.on('connect', function () {
    socket.emit('is_connected', {data: 'I\'m connected!'});
    console.log("connected");

    console.log(quiz_id);

    socket.emit('join_game', {"quiz_id": quiz_id});
    socket.emit('get_current_question', {"quiz_id": quiz_id, "user_id": user_id})
  });

  socket.on('message', function (message) {
    console.log(message)
  });

  socket.on('disconnect', function () {
    socket.emit('leave_game', {"quiz_id": quiz_id});
    console.log("Socket disconnected")
  });

  socket.on('current_question', function (data) {
    console.log(data);
    document.getElementById("quiz-question").innerHTML = data["question"];

    for (i in data["answers"]) {
      document.getElementById("answer-button-" + i.toString()).innerHTML = data["answers"][i]["answer_text"];
      document.getElementById("answer-button-" + i.toString()).onclick = function () {
        socket.emit("send_answer", {
          "user_id": user_id,
          "quiz_id": quiz_id,
          "answer_id": data["answers"][i]["answer_id"]
        })
      };
    }
  });

  socket.on('received_answer', function (data) {
    console.log(data);
    document.getElementById("answer_form").style.display = "none";
    document.getElementById("sent_answer").innerHTML = "Wait for the next question...";
  })


});