
const taskInput = document.getElementById("taskInput");
const runButton = document.getElementById("runButton");
const result = document.getElementById("result");

runButton.addEventListener("click", runAgent);

async function runAgent() {
    const task = taskInput.value;

    if (task.trim() === "") {
        result.textContent = "Please enter a task.";
        return;
    }

    result.textContent = "Sending task to backend...";

    try {
        const response = await fetch("http://127.0.0.1:8000/agent", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                task: task
            })
        });

        const data = await response.json();

        result.textContent = data.message;

    } catch (error) {
        result.textContent = "Could not connect to the backend.";
        console.error(error);
    }
}
