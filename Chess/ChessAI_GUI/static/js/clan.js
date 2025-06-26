
document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("clan-search-form");
    if (searchForm) {
        searchForm.addEventListener("submit", function (e) {
            // Optional: Add client-side validation or AJAX call here
            console.log("Clan search form submitted.");
        });
    }
});
