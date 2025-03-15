document.addEventListener("DOMContentLoaded", function () {

    // Animation for the navigation menu
    gsap.from("nav ul li", {
        opacity: 0,
        y: -20,
        duration: 0.8,
        stagger: 0.15,
        ease: "power2.out"
    });

    // Animation for the logo
    gsap.from(".app-logo", {
        opacity: 0,
        scale: 0.8,
        duration: 1,
        ease: "back.out(1.7)"
    });

    // Animation for the login form and inputs
    gsap.from(".login-container h1", {
        opacity: 0,
        y: -30,
        duration: 1,
        ease: "power2.out"
    });

    gsap.from(".login-container input", {
        opacity: 0,
        y: 30,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out"
    });

    gsap.from(".login-container button", {
        opacity: 0,
        y: 30,
        duration: 0.8,
        delay: 0.3,
        ease: "power2.out"
    });

    // Animation for forgot password and sign up links
    gsap.from(".forgot-password, .sign_up", {
        opacity: 0,
        y: 20,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out"
    });

    // Animation for footer links and icon
    gsap.from("footer ul li", {
        opacity: 0,
        y: 20,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out"
    });

    gsap.from("footer .icon", {
        opacity: 0,
        scale: 0.8,
        duration: 1,
        ease: "power2.out"
    });

});
