document.addEventListener("DOMContentLoaded", function() {
    const chatboxContainer = document.getElementById("chatbox-container");
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");

    // Function to send user input to backend
    function sendMessageToBackend(message) {
        // Assuming you're using fetch API to send data to Django backend
        fetch("/send-message/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            // Display response in chatbox
            displayMessage(data.response, "bot");
        })
        .catch(error => {
            console.error("Error sending message to backend:", error);
        });
    }

    // Function to display messages in the chatbox
    function displayMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        if (sender === "user") {
            messageElement.classList.add("user-message");
        } else {
            messageElement.classList.add("bot-message");
        }
        messageElement.textContent = message;
        chatboxContainer.appendChild(messageElement);
        // Scroll chatbox to bottom
        chatboxContainer.scrollTop = chatboxContainer.scrollHeight;
    }

    // Event listener for send button click
    sendButton.addEventListener("click", function() {
        const message = userInput.value.trim();
        if (message !== "") {
            displayMessage(message, "user");
            sendMessageToBackend(message);
            userInput.value = ""; // Clear input field
        }
    });

    // Toggle chatbox visibility
    function toggleChatbox() {
        const chatbox = document.getElementById("chatbox");
        chatbox.classList.toggle("open");
    }
});