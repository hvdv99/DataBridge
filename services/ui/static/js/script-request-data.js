
// This script is used to send data from the form to the server using the fetch API.
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("requestDataForm");
    const button = document.getElementById("requestDataButton");
    const messageDiv = document.getElementById("submissionMessage");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Gather the form data
        const formData = new FormData(form);

        // Send the data using fetch API
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json()) // Make sure the response is processed as JSON
            .then(data => {
                // Assuming the response includes {"success": true, "message": "..."}
                if (data.success) {
                    button.style.backgroundColor = "grey"; // Change button color
                    button.disabled = true; // Make button unclickable
                    messageDiv.innerText = data.message; // Display the message from the server
                } else {
                    // Handle the case where success is not true
                    messageDiv.innerText = "There was an issue with your request.";
                }
            })
            .catch(error => console.error('There has been a problem with your fetch operation:', error));
    });
});