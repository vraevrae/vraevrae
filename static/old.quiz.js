const socket = io.connect('http://' + document.domain + ':' + location.port);

function updateForm(wait = false) {
    if (wait) {
        document.getElementById("answer_form").style.display = "none";
        document.getElementById("sent_answer").innerHTML = "Wait for the next question...";
    } else {
        document.getElementById("answer_form").style.display = "block";
        document.getElementById("sent_answer").innerHTML = "";
    }
}

function get_new_question(quiz_id, user_id) {
    console.log("GET NEW QUESTION", quiz_id, user_id);
    socket.emit('get_current_question', {"quiz_id": quiz_id, "user_id": user_id});
}

$(document).ready(function () {
    updateForm(false);
    let quiz_id = document.getElementById("data").dataset.quiz_id;
    let user_id = document.getElementById("data").dataset.user_id;

    console.log(quiz_id, user_id);

    let progress_timer = setInterval(update_timer, 1000);

    get_new_question(quiz_id, user_id);

    function fill_template(quiz_id, user_id, question, answers) {
        console.log("FILL TEMPLATE");
        progress_timer = setInterval(update_timer, 1000);

        document.getElementById("quiz-question").innerHTML = question;

        for (let i in answers) {
            document.getElementById("answer-button-" + i.toString()).innerHTML = answers[i]["answer_text"];
            document.getElementById("answer-button-" + i.toString()).onclick = function () {
                socket.emit("send_answer", {
                    "user_id": user_id,
                    "quiz_id": quiz_id,
                    "answer_id": answers[i]["answer_id"]
                })
            };
        }
    );
}

function check_timer() {
    let current_progress = document.getElementById("progress_bar").position;

    if (current_progress === 0) {
        get_new_question(quiz_id, user_id);
        updateForm(false);
        clearInterval(progress_timer)
    }
}

function update_timer() {
    let current_progress = document.getElementById("progress_bar").position;

    document.getElementById("progress_bar").value = current_progress - 10;
}

socket.on('connect', function () {
    socket.emit('is_connected', {data: 'I\'m connected!'});
    console.log("connected");

    console.log(quiz_id);

    socket.emit('join_game', {"quiz_id": quiz_id});
    get_new_question(quiz_id, user_id);
});

socket.on('message', function (message) {
    console.log(message)
});

socket.on('disconnect', function () {
    socket.emit('leave_game', {"quiz_id": quiz_id});
    console.log("Socket disconnected")
});

socket.on('current_question', function (data) {
    console.log("CURRENT Q", data);

    fill_template(quiz_id, user_id, data["question"], data["answers"]);
});

socket.on('received_answer', function (data) {
    console.log("RECEIVED ANSWER", data);
    updateForm(true)
});
})