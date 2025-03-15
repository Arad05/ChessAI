document.addEventListener("DOMContentLoaded", function () {
    // Navigation animation using gsap
    gsap.from("nav ul li", {
        opacity: 0,
        y: -20,
        duration: 0.8,
        stagger: 0.15,
        ease: "power2.out"
    });

    // Form appearance effect
    gsap.from(".sign-up-container", {
        opacity: 0,
        scale: 0.9,
        duration: 1,
        ease: "power3.out"
    });

    // Sign Up button animation on hover
    const signUpButton = document.querySelector("button[type='submit']");
    signUpButton.addEventListener("mouseover", () => {
        gsap.to(signUpButton, {
            scale: 1.1,
            backgroundColor: "#ffcc00",
            boxShadow: "0px 10px 20px rgba(0, 0, 0, 0.3)",
            duration: 0.3,
            ease: "power2.out"
        });
    });

    signUpButton.addEventListener("mouseleave", () => {
        gsap.to(signUpButton, {
            scale: 1,
            backgroundColor: "#ff9900",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
            duration: 0.3,
            ease: "power2.out"
        });
    });

    // Input fields effect on focus/blur
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

const app = Vue.createApp({
    data() {
        return {
            email: '',
            password: '',
            first_name: '',
            last_name: '',
            nickname: '',  // New field for nickname
            phone_number: '',
            country: '',
            errorMessage: '',
            csrf_token: document.querySelector('meta[name="csrf_token"]')
                        ? document.querySelector('meta[name="csrf_token"]').getAttribute('content')
                        : '',
        };
    },
    methods: {
        async submit_Sign_up() {
            try {
                const response = await fetch('/sign_up', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrf_token,
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                        first_name: this.first_name,
                        last_name: this.last_name,
                        nickname: this.nickname,  // Include nickname in signup data
                        phone_number: this.phone_number,
                        country: this.country,
                    })
                });

                if (!response.ok) {
                    throw new Error('Request failed with status ' + response.status);
                }

                const result = await response.json();

                if (result.success) {
                    alert(result.message);
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error(error);
                this.errorMessage = "שגיאה בחיבור לשרת.";
            }
        }
    }
});

app.mount('#app');
