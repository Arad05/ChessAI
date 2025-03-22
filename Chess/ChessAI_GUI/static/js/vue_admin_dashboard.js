document.addEventListener("DOMContentLoaded", function () {
    // Animate header navigation links
    gsap.from("header nav ul li", {
        opacity: 0,
        y: -20,
        stagger: 0.2,
        duration: 0.8,
        ease: "power2.out",
    });

    // Animate table rows
    gsap.from("table tbody tr", {
        opacity: 0,
        y: 20,
        stagger: 0.1,
        duration: 0.8,
        ease: "power2.out",
    });


    // Animate page title
    gsap.from(".page-title", {
        opacity: 0,
        y: -30,
        duration: 1,
        ease: "power3.out",
    });

    // Button hover animation
    const buttons = document.querySelectorAll(".action-btn");
    buttons.forEach((button) => {
        button.addEventListener("mouseenter", () => {
            gsap.to(button, { scale: 1.1, duration: 0.3 });
        });
        button.addEventListener("mouseleave", () => {
            gsap.to(button, { scale: 1, duration: 0.3 });
        });
    });

    // Modal animations
    const modal = document.getElementById("banModal");
    const modalContent = modal.querySelector(".modal-content");

    // Show the modal with animation
    function openModal() {
        modal.style.display = "block";
        gsap.from(modalContent, {
            opacity: 0,
            scale: 0.8,
            duration: 0.5,
            ease: "power2.out"
        });
    }

    // Close the modal with animation
    function closeModal() {
        gsap.to(modalContent, {
            opacity: 0,
            scale: 0.8,
            duration: 0.3,
            ease: "power2.in",
            onComplete: () => {
                modal.style.display = "none";
            }
        });
    }

    // Close modal when the close button is clicked
    const closeButton = document.querySelector(".close");
    if (closeButton) {
        closeButton.addEventListener("click", closeModal);
    }

    // Spinner rotation animation
    const spinner = document.querySelector(".spinner");
    if (spinner) {
        gsap.to(spinner, {
            rotation: 360,
            repeat: -1,  // infinite loop
            duration: 2,
            ease: "linear"
        });
    }
});
