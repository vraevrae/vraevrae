$(document).ready(function() {
  let current_progress = 100

  let interval = setInterval(function() {
    current_progress -= 10
    $('#quiz-progress')
      .css('width', `${current_progress}%`)
      .attr('aria-valuenow', current_progress)

    if (current_progress === 0) {
      location.reload();
      clearInterval(interval)
    }
  }, 1000)

  $('.answerbtn').click(function(e) {

    data = {
      action: 'answer',
      answer_id: e.currentTarget.value
    }

    $.ajax({
      type: 'POST',
      url: '/game',
      data: data, // serializes the form's elements.
      success: function() {
        document.getElementById('update').innerHTML = "Wait for the next question..."
        // var d1 = document.getElementById('update');
        // d1.insertAdjacentHTML('afterend', '<div id="updated">WAIT FOR QUESTION</div>');
        /// d1.parentNode.removeChild(d1);
      }
    })

    return false // avoid to execute the actual submit of the form.
  })
})
