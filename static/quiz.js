$(document).ready(function() {
  let current_progress = 100

  let interval = setInterval(function() {
    current_progress -= 10
    $('#quiz-progress')
      .css('width', `${current_progress}%`)
      .attr('aria-valuenow', current_progress)

    if (current_progress === 0) {
      /*location.reload();*/
      clearInterval(interval)
    }
  }, 1000)

  $('.answerbtn').click(function(e) {
    console.log('answerbtn run')

    data = {
      action: 'answer',
      answer_id: e.currentTarget.value
    }

    $.ajax({
      type: 'POST',
      url: '/game',
      data: data, // serializes the form's elements.
      success: function() {
        document.getElementById('update').innerHTML = 'HALLO'
      }
    })

    return false // avoid to execute the actual submit of the form.
  })
})
