$(function () {
    const socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        socket.emit('is_connected', {data: 'I\'m connected!'});
        console.log("connected");

        let game_id;
        game_id = document.getElementById("game_id").dataset.game_id.toString();

        console.log(game_id);

        socket.emit('join_game', {"game_id": game_id})
    });

    socket.on('message', function (message) {
        console.log(message)
    })
});
