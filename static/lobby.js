function game_started(game_id) {
    window.setInterval(function () {
        fetch('/api/game/started/' + game_id.toString())
            .then(
                function (response) {
                    if (response.status !== 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                            response.status);

                        location.href("/");

                        return;
                    }

                    // Examine the text in the response
                    response.json().then(function (data) {
                        console.log(data);

                        data.data.has_started && location.reload(false)
                    });
                }
            )
            .catch(function (err) {
                console.log('Fetch Error :-S', err);
            });
    }, 1200);
}

document.onload = game_started(document.getElementById("game_id").dataset.game_id);