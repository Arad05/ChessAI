document.addEventListener("DOMContentLoaded", function() {
    // Role Management
    const roleElement = document.getElementById('role');
    const role = roleElement.innerText.trim().toLowerCase();

    const roleNames = {
        'admin': 'Admin',
        'user': 'Rookie',
        'member': 'Member'
    };
    roleElement.innerText = roleNames[role] || 'Rookie';

    const roleColors = {
        'admin': 'admin-role',
        'user': 'rookie-role',
        'member': 'member-role'
    };
    roleElement.classList.add(roleColors[role] || 'user-role');

    // Friend and History List Expanding/Collapsing Logic
    let friendLimit = 5;
    let historyLimit = 5;

    const friends = Array.from(document.querySelectorAll(".friend-card"));
    const historyRows = Array.from(document.querySelectorAll(".history-table tbody tr"));

    const showMoreFriendsButton = document.getElementById("showMoreFriends");
    const collapseFriendsButton = document.getElementById("collapseFriends");
    const showMoreHistoryButton = document.getElementById("showMoreHistory");
    const collapseHistoryButton = document.getElementById("collapseHistory");

    function updateFriendList() {
        friends.forEach((friend, index) => {
            friend.style.display = index < friendLimit ? "block" : "none";
        });

        showMoreFriendsButton.style.display = friendLimit < friends.length ? "block" : "none";
        collapseFriendsButton.style.display = friendLimit > 5 ? "block" : "none";
    }

    function updateHistoryList() {
        historyRows.forEach((row, index) => {
            row.style.display = index < historyLimit ? "table-row" : "none";
        });

        showMoreHistoryButton.style.display = historyLimit < historyRows.length ? "block" : "none";
        collapseHistoryButton.style.display = historyLimit > 5 ? "block" : "none";
    }

    showMoreFriendsButton?.addEventListener("click", function() {
        friendLimit += 5;
        updateFriendList();
    });

    collapseFriendsButton?.addEventListener("click", function() {
        friendLimit = 5;
        updateFriendList();
    });

    showMoreHistoryButton?.addEventListener("click", function() {
        historyLimit += 5;
        updateHistoryList();
    });

    collapseHistoryButton?.addEventListener("click", function() {
        historyLimit = 5;
        updateHistoryList();
    });

    // Initial updates
    updateFriendList();
    updateHistoryList();
});
