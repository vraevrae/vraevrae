$(document).ready(function() {
    let current_progress = 100;
    
    let interval = setInterval(function () {
        current_progress -= 10;
        $("#quiz-progress")
        .css("width", `${current_progress}%`)
        .attr("aria-valuenow", current_progress);

        if (current_progress === 0){
            /*location.reload();*/
            clearInterval(interval);
        }
    }, 1000);

    $("#.answerbtn").click(function(e) {
        console.log("hallo");
        var url = "/game"; // the script where you handle the form input.
        console.log($("#update").serialize());
        // $.ajax({
        //     type: "POST",
        //     url: url,
        //     data: {'data':$("#update").serialize()}, // serializes the form's elements.
        //     success: function()
        //     {
        //         document.getElementById("update").innerHTML = "HALLO"
        //         var elem = document.getElementById('button');
        //         elem.parentNode.removeChild(elem);
        //     }
        //     });

        return false; // avoid to execute the actual submit of the form.
    });
});