document.addEventListener("DOMContentLoaded", function () {
    // אנימציה לתפריט הניווט
    gsap.from("nav ul li", {
        opacity: 0,
        y: -20,
        duration: 0.8,
        stagger: 0.15,
        ease: "power2.out"
    });

    // אפקט הופעה לטופס השחזור (מותאם לשם הנכון)
    gsap.from(".forgot-password-container", {
        opacity: 0,
        scale: 0.9,
        duration: 1,
        ease: "power3.out"
    });


    // אפקט לפוקוס בשדות הקלט
    document.querySelectorAll("input").forEach(input => {
        input.addEventListener("focus", () => {
            gsap.to(input, {
                backgroundColor: "#f0f8ff",
                borderColor: "#007bff",
                duration: 0.3,
                ease: "power2.out"
            });
        });

        input.addEventListener("blur", () => {
            gsap.to(input, {
                backgroundColor: "#fff",
                borderColor: "#ccc",
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });
});
