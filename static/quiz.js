$(document).ready(function() {
    let current_progress = 100;
    const socket = io.connect('http://' + document.domain + ':' + location.port);
    let quiz_id = document.getElementById("quiz_id").dataset.quiz_id;

  let interval = setInterval(function() {
      current_progress -= 10;
    $('#quiz-progress')
      .css('width', `${current_progress}%`)
        .attr('aria-valuenow', current_progress);

    if (current_progress === 0) {
      location.reload();
      clearInterval(interval)
    }
  }, 1000);


    socket.on('connect', function () {
        socket.emit('is_connected', {data: 'I\'m connected!'});
        console.log("connected");

        console.log(quiz_id);

        socket.emit('join_game', {"quiz_id": quiz_id})
    });

    socket.on('message', function (message) {
        console.log(message)
    });

    socket.on('disconnect', function () {
        socket.emit('leave_game', {"quiz_id": quiz_id});
        console.log("Socket disconnected")
    });

    socket.on('get_current_question', function (data) {
        document.getElementById("quiz-question").innerHTML = data["question"];

        for (let i = 0; i < data["answers"].length(); i++) {
            document.getElementById("answer-button-" + i.toString()).innerHTML = data["answers"][i]
        }
  })

});
