document.addEventListener("DOMContentLoaded", function () {
    // הדגשת קישור פעיל בתפריט
    const currentLocation = window.location.pathname;
    document.querySelectorAll("nav ul li a").forEach(link => {
        if (link.getAttribute("href") === currentLocation) {
            link.classList.add("active");
        }
    });

    // אנימציה להופעת הניווט עם GSAP
    gsap.from("nav ul li", {
        opacity: 0,
        y: -20,
        duration: 0.8,
        stagger: 0.15,
        ease: "power2.out"
    });

    // אפקט hover מתקדם לכפתורים
    document.querySelectorAll(".play-button").forEach(button => {
        button.addEventListener("mouseover", () => {
            gsap.to(button, {
                scale: 1.1,
                boxShadow: "0px 10px 20px rgba(0, 0, 0, 0.3)",
                duration: 0.3,
                ease: "power2.out"
            });
        });

        button.addEventListener("mouseleave", () => {
            gsap.to(button, {
                scale: 1,
                boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });
});
