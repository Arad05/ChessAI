const app = Vue.createApp({
    data() {
        return {
            email: '',
            password: '',
            first_name: '',
            last_name: '',
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
