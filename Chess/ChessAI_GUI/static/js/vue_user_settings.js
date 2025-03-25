const app = Vue.createApp({
  data() {
    return {
      user: initialUserData || {
        nickname: "OriK",
        phone: "053-225-7111",
        name: "Ori",
        lastName: "Kopilov",
        role: "Admin",
        friends: ["NotSamur", "JohnD", "Extra1", "Extra2", "Extra3", "Extra4"], // Sample data
        country: "Israel",
        stats: { wins: 10, draws: 5, losses: 3 },
        csrf_token: document.querySelector('meta[name="csrf_token"]')
          ? document.querySelector('meta[name="csrf_token"]').getAttribute('content')
          : "",
        history: [
          { opponent: "Arad Or", result: "win", date: "2025-03-12 15:30" },
          { opponent: "John Doe", result: "draw", date: "2025-03-11 20:15" },
          { opponent: "Extra Opp 1", result: "loss", date: "2025-03-10 20:15" },
          { opponent: "Extra Opp 2", result: "win", date: "2025-03-09 20:15" },
          { opponent: "Extra Opp 3", result: "win", date: "2025-03-08 20:15" },
          { opponent: "Extra Opp 4", result: "draw", date: "2025-03-07 20:15" }
        ]
      },
      friendLimit: 5,
      historyLimit: 5
    };
  },
  computed: {
    roleClass() {
      const validRoles = ["Rookie", "member", "admin"];
      return validRoles.includes(this.user.role) ? this.user.role : 'Rookie';
    },
    limitedHistory() {
      return this.user.history.slice(0, this.historyLimit);
    },
    limitedFriends() {
      return this.user.friends.slice(0, this.friendLimit);
    },
    showMoreFriendsButton() {
      return this.friendLimit < this.user.friends.length;
    },
    showCollapseFriendsButton() {
      return this.friendLimit > 5;
    },
    showMoreHistoryButton() {
      return this.historyLimit < this.user.history.length;
    },
    showCollapseHistoryButton() {
      return this.historyLimit > 5;
    }
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
    },
    showMoreFriends() {
      this.friendLimit += 5;
    },
    collapseFriends() {
      this.friendLimit = 5;
    },
    showMoreHistory() {
      this.historyLimit += 5;
    },
    collapseHistory() {
      this.historyLimit = 5;
    },

    formatPhone() {
      let digits = this.user.phone.replace(/\D/g, ''); // הסרת תווים לא מספריים
      if (digits.length <= 3) {
        this.user.phone = digits;
      } else if (digits.length <= 6) {
        this.user.phone = `${digits.slice(0, 3)}-${digits.slice(3)}`;
      } else if (digits.length <= 10) {
        this.user.phone = `${digits.slice(0, 3)}-${digits.slice(3, 6)}-${digits.slice(6)}`;
      } else {
        this.user.phone = `${digits.slice(0, 3)}-${digits.slice(3, 6)}-${digits.slice(6, 10)}`;
      }
    },
  }
});

app.mount('#app');
