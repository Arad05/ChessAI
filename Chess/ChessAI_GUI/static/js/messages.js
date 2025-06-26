document.addEventListener("DOMContentLoaded", function () {
    const sendBtn = document.getElementById("sendBtn");
    const textarea = document.getElementById("messageInput");
    const messagesContainer = document.getElementById("messagesBox");

    function sendMessage(friendNickname) {
        const message = textarea.value.trim();
        console.log("Sending to:", friendNickname, "Message:", message);
        if (!message) return;
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch("/send_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ to: friendNickname, message: message })
        })
        .then(res => res.json().catch(() => {
            throw new Error("Invalid JSON returned from server");
        }))
        .then(data => {
            if (data.success) {
                const msgElement = document.createElement("div");
                msgElement.className = "message-box sent";
                const now = new Date().toISOString().slice(0, 19).replace("T", " ");
                msgElement.innerHTML = `
                    <div class="meta">You | ${now}</div>
                    <div class="text">${message}</div>`;
                messagesContainer.appendChild(msgElement);
                textarea.value = "";
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(err => {
            console.error("Failed to send message:", err);
            alert("Failed to send message. Please check the console.");
        });
    }

    sendBtn.addEventListener("click", () => {
        const friendNickname = sendBtn.dataset.friend;
        sendMessage(friendNickname);
    });
});
