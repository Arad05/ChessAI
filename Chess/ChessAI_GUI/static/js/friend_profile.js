document.addEventListener("DOMContentLoaded", function() {
    // Get the role element
    const roleElement = document.getElementById('role');
    const role = roleElement.innerText.trim().toLowerCase();

    // Map roles to their respective display names
    const roleNames = {
        'admin': 'Admin',
        'user': 'Rookie',
        'member': 'Member'
    };

    // Set the role to the corresponding name or default to 'Rookie'
    const roleName = roleNames[role] || 'Rookie';

    // Update the role element text with the mapped role name
    roleElement.innerText = roleName;

    // Define role color mappings
    const roleColors = {
        'admin': 'admin-role',
        'user': 'rookie-role',
        'member': 'member-role'
    };

    // Check if the role exists in the mappings, otherwise default to 'user-role'
    const roleClass = roleColors[role] || 'user-role';

    // Add the role class to the span for styling
    roleElement.classList.add(roleClass);
});
