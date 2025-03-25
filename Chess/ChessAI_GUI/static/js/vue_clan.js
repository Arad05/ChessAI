// vue_clans.js

document.addEventListener("DOMContentLoaded", function () {
    // Initialize Vue on the main container (excluding nav and footer)
    new Vue({
      el: '#clan-app',
      data: {
        // You could extend this data with dynamic information if needed
        animationActive: true
      },
      mounted() {
        // Simple mounted hook to log or trigger additional animations if needed
        console.log("Vue clan app mounted and animations active.");
      },
      methods: {
        // Additional methods can be added here for interactive animations
      }
    });
  });
  