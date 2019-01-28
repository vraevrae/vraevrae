$(function () {
    const socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit('is_connected', {data: 'I\'m connected!'});
        console.log("connected");

        let quiz_id;
        quiz_id = document.getElementById("quiz_id").dataset.quiz_id;

        console.log(quiz_id);

        socket.emit('join_game', {"quiz_id": quiz_id})
    });

    socket.on('start_game', function () {
        console.log("start game");
        location.reload(false)
    });

    socket.on('message', function (message) {
        console.log(message)
    });

    socket.on('disconnect', function () {
        console.log("Socket disconnected")
    });
});
