// about.js
// Similar functionality for button animations

const app = Vue.createApp({
    methods: {
        animateButton(event) {
            event.target.style.transform = 'scale(1.1)';
        },
        resetButton(event) {
            event.target.style.transform = 'scale(1)';
        }
    }
});

app.mount('#app');
