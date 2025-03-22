document.addEventListener("DOMContentLoaded", function () {
    gsap.set("main", { opacity: 0 });
    
    // הצגת התוכן בצורה הדרגתית
    gsap.to("main", { opacity: 1, duration: 1.2, ease: "power2.out" });

    // אנימציה לתפריט ניווט
    gsap.from("nav ul li", {
        opacity: 0,
        y: -30,
        duration: 1,
        stagger: 0.2,
        ease: "power3.out"
    });

    // אפקט hover משופר לכפתורים
    document.querySelectorAll(".play-button").forEach(button => {
        button.addEventListener("mouseover", () => {
            gsap.to(button, {
                scale: 1.15,
                rotate: 2,
                boxShadow: "0px 12px 25px rgba(0, 0, 0, 0.4)",
                duration: 0.4,
                ease: "power2.out"
            });
        });

        button.addEventListener("mouseleave", () => {
            gsap.to(button, {
                scale: 1,
                rotate: 0,
                boxShadow: "0px 5px 8px rgba(0, 0, 0, 0.2)",
                duration: 0.4,
                ease: "power2.out"
            });
        });
    });

    // אנימציה ללוגו
    gsap.from(".app-logo", {
        opacity: 0,
        y: -50,
        scale: 0.8,
        duration: 1.2,
        ease: "elastic.out(1, 0.6)"
    });

    // אנימציה לכותרת
    gsap.from(".title-container", {
        opacity: 0,
        y: 20,
        duration: 1,
        delay: 0.5,
        ease: "power2.out"
    });
});
