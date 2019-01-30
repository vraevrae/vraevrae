window.onload = () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);
    let quiz_id = document.getElementById("data").dataset.quiz_id;
    let user_id = document.getElementById("data").dataset.user_id;


    socket.on('connect', function () {
        socket.emit('is_connected', {data: 'I\'m connected!'});
        console.log("connected");

        console.log(quiz_id);

        socket.emit('join_game', {"quiz_id": quiz_id, "user_id": user_id})
    });

    socket.on('message', function (message) {
        console.log(message)
    });

    socket.on('disconnect', function () {
        socket.emit('leave_game', {"quiz_id": quiz_id});
        console.log("Socket disconnected")
    });

    socket.on('current_players', function (data) {
        console.log("current_players: ", data);
    });
};
