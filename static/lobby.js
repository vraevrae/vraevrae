window.onload = () => {
  // vue templating setup en state initialisation
  var vue_player_list = new Vue({
    el: '#vue-player-list',
    data: {
      users: []
    }
  })

  // socket setup
  const socket = io.connect('http://' + document.domain + ':' + location.port)
  let { quiz_id, user_id } = document.querySelector('#data').dataset

  // connect and join game
  socket.on('connect', function() {
    socket.emit('is_connected', { data: "I'm connected!" })
    socket.emit('join_game', { quiz_id, user_id })
  })

  // disconnect
  socket.on('disconnect', function() {
    socket.emit('leave_game', { quiz_id })
  })

  // get all current players
  socket.on('current_players', function(data) {
    vue_player_list.users = data.users
  })

  // when the game starts reload to get proper template
  socket.on('start_game', function(data) {
    window.location.reload()
  })
}
