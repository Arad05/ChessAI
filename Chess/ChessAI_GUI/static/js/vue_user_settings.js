const app = Vue.createApp({
    data() {
        return {
            user: {
                email: "orikopilov2007@gmail.com",
                phone: "053-225-7111",
                name: "Ori",
                lastName: "Kopilov",
                friends: ["Arad Or", "John Doe"],
                country: "Isreal",
                stats: {
                    wins: 10,
                    draws: 5,
                    losses: 3
                },
                history: [
                    {"opponent": "Arad Or", "result": "win", "date": "2025-03-12 15:30"},
                    {"opponent": "John Doe", "result": "draw", "date": "2025-03-11 20:15"}
                ]
            }
        };
    }
});

app.mount('#app');
