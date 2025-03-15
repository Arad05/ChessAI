const app = Vue.createApp({
  data() {
    return {
      user: initialUserData || {
        nickname: "OriK",
        phone: "053-225-7111",
        name: "Ori",
        lastName: "Kopilov",
        friends: [
          { nickname: "NotSamur", name: "Arad Or" },
          { nickname: "JohnD", name: "John Doe" }
        ],
        country: "Israel",
        stats: { wins: 10, draws: 5, losses: 3 },
        csrf_token: document.querySelector('meta[name="csrf_token"]')
          ? document.querySelector('meta[name="csrf_token"]').getAttribute('content')
          : "",
        history: [
          { opponent: "Arad Or", result: "win", date: "2025-03-12 15:30" },
          { opponent: "John Doe", result: "draw", date: "2025-03-11 20:15" }
        ]
      }
    };
  },
  methods: {
    updateSettings() {
      fetch('/update_user_settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.user.csrf_token
        },
        body: JSON.stringify(this.user)
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('Settings updated successfully!');
        } else {
          alert('Error updating settings: ' + data.error);
        }
      })
      .catch(error => {
        console.error(error);
        alert('Error updating settings.');
      });
    }
  }
});
app.mount('#app');
