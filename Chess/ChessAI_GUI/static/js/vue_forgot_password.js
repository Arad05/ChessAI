document.addEventListener("DOMContentLoaded", function () {
    
    // אנימציה לתפריט הניווט
    gsap.from("nav ul li", {
        opacity: 0,
        y: -20,
        duration: 0.8,
        stagger: 0.15,
        ease: "power2.out"
    });

    // אפקט הופעה ללוגו
    gsap.from(".app-logo", {
        opacity: 0,
        scale: 0.8,
        duration: 1,
        ease: "back.out(1.7)"
    });

    // אפקט הופעה לטופס השחזור
    gsap.from(".forgot-password-container", {
        opacity: 0,
        y: 30,
        duration: 1,
        ease: "power2.out"
    });

    // אנימציה לכפתורי השליחה
    document.querySelectorAll("button[type='submit']").forEach(button => {
        button.addEventListener("mouseover", () => {
            gsap.to(button, {
                scale: 1.1,
                backgroundColor: "#ffcc00",
                boxShadow: "0px 10px 20px rgba(0, 0, 0, 0.3)",
                duration: 0.3,
                ease: "power2.out"
            });
        });

        button.addEventListener("mouseleave", () => {
            gsap.to(button, {
                scale: 1,
                backgroundColor: "#ff9900",
                boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });

    // אנימציה לקישורים בפוטר
    gsap.from("footer ul li", {
        opacity: 0,
        y: 20,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out"
    });

    // אנימציה לאייקון בפוטר
    gsap.from("footer .icon", {
        opacity: 0,
        scale: 0.8,
        duration: 1,
        ease: "power2.out"
    });

});
