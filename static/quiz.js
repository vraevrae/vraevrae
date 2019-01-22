$(function() {
    let current_progress = 100;
    
    let interval = setInterval(function () {
        current_progress -= 10;
        $("#quiz-progress")
        .css("width", `${current_progress}%`)
        .attr("aria-valuenow", current_progress);

        if (current_progress === 0){
            clearInterval(interval);
            window.location.href = window.location.pathname + window.location.search + window.location.hash;
        }
    }, 1000);
  });



