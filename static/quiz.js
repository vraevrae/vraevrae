var time = document.getElementById("time");

function plusOne()
{
    time.appendChild(document.createTextNode('I'));
}

function showPage(){
    window.location.href = 'test.html';
}

// window.setInterval(plusOne, 1000);
// setTimeout(showPage, 10000);

/* Register Letter user clicked on */

function send_answer(letter) {
	xmlrequest("answer?letter=" + letter,
		function() {
			if (this.readyState == 4 && this.status == 200) {
				switch_screens();
                state = "wait_question";
            }
		}
	);
}

$('.button_B').click(function(e) {
    $('.Button').not(this).removeClass('active');    
    $(this).toggleClass('active');
    e.preventDefault();
});

$(function() {
    var current_progress = 100;
    var interval = setInterval(function() {
        current_progress -= 10;
        $("#quiz-progress")
        .css("width", `${current_progress}%`)
        .attr("aria-valuenow", current_progress);
        if (current_progress == 0)
            clearInterval(interval);
    }, 1000);
  });