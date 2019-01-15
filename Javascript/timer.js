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

