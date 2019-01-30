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

    socket.on('new_player', function (data) {
        console.log("new player: ", data);
        let username = data["username"];
        let list_el = document.createElement("li");
        list_el.innerHTML = username;
        list_el.setAttribute("class", "list-group-item");

        console.log(list_el);
        console.log(document.getElementById("player_list"));

        document.getElementById("player_list").appendChild(list_el);
    });
};
