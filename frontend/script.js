const runButton = document.getElementById("runButton");

const taskInput = document.getElementById("taskInput");

const result = document.getElementById("result");


runButton.addEventListener("click", async function () {

    const task = taskInput.value;

    result.innerText = "Connecting to backend...";

    const response = await fetch("http://127.0.0.1:8000/");

    const data = await response.json();

    result.innerText = data.message;

});