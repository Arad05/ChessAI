document.addEventListener("DOMContentLoaded", function () {
    const { createApp } = Vue;

    createApp({
        methods: {
            animateButton(event) {
                gsap.to(event.target, {
                    scale: 1.1,
                    boxShadow: "0px 10px 20px rgba(0, 0, 0, 0.3)",
                    duration: 0.3,
                    ease: "power2.out"
                });
            },
            resetButton(event) {
                gsap.to(event.target, {
                    scale: 1,
                    boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                    duration: 0.3,
                    ease: "power2.out"
                });
            }
        }
    }).mount("#app");
});
