document.addEventListener("DOMContentLoaded", function() {
  const actionButtons = document.querySelectorAll(".action-btn");
  const banModal = document.getElementById("banModal");
  const closeModal = document.querySelector(".modal .close");
  let currentTargetEmail = null;

  // Get CSRF token from the meta tag
  const csrfToken = document.querySelector('meta[name="csrf_token"]').getAttribute('content');

  // Listen for clicks on action buttons
  actionButtons.forEach(function(button) {
    button.addEventListener("click", function() {
      const action = button.getAttribute("data-action");
      const targetEmail = button.getAttribute("data-email");
      if (action === "ban") {
        currentTargetEmail = targetEmail;
        // Open modal to enter ban duration
        banModal.style.display = "block";
      } else if (action === "promote") {
        // Handle the promote action (for admin)
        if (confirm(`Are you sure you want to promote ${targetEmail} to member?`)) {
          sendAdminAction(action, targetEmail);
        }
      } else {
        // Confirmation for demote, delete
        if (confirm(`Are you sure you want to ${action} the user?`)) {
          sendAdminAction(action, targetEmail);
        }
      }
    });
  });

  // Close the modal when clicking on the close span
  closeModal.addEventListener("click", function() {
    banModal.style.display = "none";
    currentTargetEmail = null;
  });

  // When clicking outside the modal content, close the modal
  window.addEventListener("click", function(event) {
    if (event.target == banModal) {
      banModal.style.display = "none";
      currentTargetEmail = null;
    }
  });

  // Confirm ban button action
  document.getElementById("confirmBan").addEventListener("click", function() {
    const duration = document.getElementById("banDuration").value;
    if (!duration || duration < 1) {
      alert("Please enter a valid ban duration in minutes.");
      return;
    }
    if (confirm(`Are you sure you want to ban this user for ${duration} minute(s)?`)) {
      sendAdminAction("ban", currentTargetEmail, duration);
      banModal.style.display = "none";
      currentTargetEmail = null;
    }
  });

  // Function to send an admin action using AJAX POST
  function sendAdminAction(action, targetEmail, duration=0) {
    const formData = new FormData();
    formData.append("action", action);
    formData.append("target_email", targetEmail);
    if (action === "ban") {
      formData.append("duration", duration);
    }

    // If promoting, make sure to hit the promote endpoint
    if (action === "promote") {
      fetch("/promote_to_member", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrfToken  // Include the CSRF token in the headers
        },
        body: JSON.stringify({
          admin_email: "{{ session['user'] }}",  // Use current session's user as admin
          target_email: targetEmail
        })
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        window.location.reload();
      })
      .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while performing the action.");
      });
      return;  // Exit the function to prevent calling the generic sendAdminAction
    }

    fetch("/admin_dashboard", {
      method: "POST",
      headers: {
        'X-CSRF-TOKEN': csrfToken  // Include the CSRF token in the headers
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      // Optionally, reload the page to update the table.
      window.location.reload();
    })
    .catch(error => {
      console.error("Error:", error);
      alert("An error occurred while performing the action.");
    });
  }
});
