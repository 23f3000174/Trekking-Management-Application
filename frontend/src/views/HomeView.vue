<template>
  <div class="home">
    <section class="hero">
      <h1>🏔️ Trekking Management Application </h1>
      <p>
      Plan, manage and track your trekking adventures.
      Browse available treks, book your next adventures, and stay updated.
      </p>

      <div v-if="!isLoggedIn">
        <button @click="$router.push('/login')">Login</button>
        <button @click="$router.push('/register')">Register as Trekker</button>
      </div>

      <div>
        <button @click="goDashboard">Go to Dashboard</button>
      </div>
    </section>

    <section class="cta">
      <p>Ready to trek?</p>
      <button @click="$router.push('/register')">Get Started →</button>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',

  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
    role() {
      return localStorage.getItem('role') || ''
    },
  },

  methods: {
    goDashboard() {
      const routes = {
        admin : '/admin/dashboard',
        staff : '/staff/dashboard',
        trekker : '/trekker/dashboard',
      }
      this.$router.push(routes[this.role] || '/login')
    },
  },

}
</script>


<style scoped>
.home {
  max-width: 1000px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  background: #2c3e50;
  color: white;
  border-radius: 8px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 2rem;
  margin-bottom: 16px;
}

.hero p {
  font-size: 1.1rem;
  margin-bottom: 24px;
  opacity: 0.9;
}

.hero button {
  margin: 6px;
  padding: 10px 24px;
  font-size: 1rem;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  background: #f39c12;
  color: white;
}

.cta {
  text-align: center;
  padding: 40px;
  background: #ecf0f1;
  border-radius: 8px;
}

.cta button {
  margin-top: 12px;
  padding: 10px 28px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}
</style>
