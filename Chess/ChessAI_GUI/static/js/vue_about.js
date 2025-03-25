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

document.addEventListener("DOMContentLoaded", function () {

    // אנימציה לתפריט הניווט
    gsap.from("nav ul li", {
        opacity: 0,
        y: -20,
        duration: 0.8,
        stagger: 0.15,
        ease: "power2.out"
    });

    // אנימציה ללוגו
    gsap.from(".app-logo", {
        opacity: 0,
        scale: 0.8,
        duration: 1,
        ease: "back.out(1.7)"
    });

    // אנימציה לכותרת הראשית
    gsap.from(".title-container", {
        opacity: 0,
        scale: 0.9,
        duration: 1,
        ease: "power2.out"
    });

    // אנימציה לטקסט של אודות
    gsap.from(".about-section h2, .about-section p", {
        opacity: 0,
        x: -50,
        duration: 1,
        stagger: 0.3,
        ease: "power2.out"
    });

    // אנימציה לרשימת התכונות
    gsap.from(".about-section ul li", {
        opacity: 0,
        x: 30,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out"
    });

    // אנימציה לכפתורי הפוטר
    gsap.from("footer ul li", {
        opacity: 0,
        y: 20,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out"
    });

});


app.mount('#app');
