const taskInput = document.getElementById("taskInput");
const runButton = document.getElementById("runButton");
const result = document.getElementById("result");

// When the user clicks the button, run the agent
runButton.addEventListener("click", runAgent);

async function runAgent() {

    // Get the task entered by the user
    const task = taskInput.value.trim();

    // Check if the user entered anything
    if (task === "") {
        result.textContent = "Please enter a task.";
        return;
    }

    // Show loading message
    result.textContent = "Gemini is generating your code...";

    // Disable button while the request is running
    runButton.disabled = true;

    try {

        // Send the task to FastAPI backend
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

        // Convert backend response into JavaScript data
        const data = await response.json();

        // Check whether backend returned an error
        if (!response.ok) {
            result.textContent =
                data.detail || "Code generation failed.";
            return;
        }

        // Display the generated code in the frontend
        result.textContent =
            data.message +
            "\n\n" +
            data.code;

        // Log the response for debugging
        console.log("Backend response:", data);

    } catch (error) {

        // Display connection or JavaScript errors
        result.textContent =
            "Could not connect to the backend. Check the browser console.";

        console.error("Frontend error:", error);

    } finally {

        // Enable button again
        runButton.disabled = false;
    }
}