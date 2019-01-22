$(function() {
    let current_progress = 100;
    
    let interval = setInterval(function () {
        current_progress -= 10;
        $("#quiz-progress")
        .css("width", `${current_progress}%`)
        .attr("aria-valuenow", current_progress);

        if (current_progress === 0){
            location.reload();
            clearInterval(interval);
        }
    }, 1000);
  });



