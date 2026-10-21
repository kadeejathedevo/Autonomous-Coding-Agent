const taskInput = document.getElementById("taskInput");
const runButton = document.getElementById("runButton");
const result = document.getElementById("result");


// Run the agent when the button is clicked.
runButton.addEventListener("click", runAgent);


async function runAgent() {

    // Get the task entered by the user.
    const task = taskInput.value.trim();

    // Check whether the task is empty.
    if (task === "") {
        result.textContent = "Please enter a task.";
        return;
    }

    // Show a message while the backend is working.
    result.textContent = "Generating your file...";

    // Prevent multiple clicks while processing.
    runButton.disabled = true;

    try {

        // Send the task to the backend.
        const response = await fetch(
            "http://127.0.0.1:8000/agent",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    task: task
                })
            }
        );

        // Convert the backend response into JavaScript data.
        const data = await response.json();

        // Display backend errors.
        if (!response.ok) {
            result.textContent = data.detail;
            return;
        }

        // Display the success message and generated code.
        result.textContent =
            data.message + "\n\n" + data.code;

    } catch (error) {

        // Display an error if the backend cannot be reached.
        result.textContent =
            "Could not connect to the backend.";

        console.error(error);

    } finally {

        // Enable the button again after processing.
        runButton.disabled = false;
    }
}