window.onload = () => {
  // vue templating setup en state initialisation
  var vue_player_list = new Vue({
    // element that contains vue template
    el: '#vue-player-list',
    // data to make reactively available to the template
    data: {
      users: []
    }
  })

  // socket setup
  const socket = io.connect('http://' + document.domain + ':' + location.port)
  let { user_id } = document.querySelector('#data').dataset

  // connect and join game
  socket.on('connect', function() {
    socket.emit('join_game', { user_id })
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
