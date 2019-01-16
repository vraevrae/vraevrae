var time = document.getElementById("time");

function plusOne()
{
    time.appendChild(document.createTextNode('I'));
}

function showPage(){
    window.location.href = 'test.html';
}

window.setInterval(plusOne, 1000);
setTimeout(showPage, 10000);


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
