<template>
  <nav v-if="showNav">
    <span @click="goHome" class="brand">
      🏔️ TrekkingApp
    </span>

    <div v-if="role === 'admin'" class="nav-links">
      <router-link to="/admin/dashboard">Dashboard</router-link>
      <router-link to="/admin/staff">Staff</router-link>
      <router-link to="/admin/treks">Treks</router-link>
      <router-link to="/admin/trekkers">Trekkers</router-link>
      <router-link to="/admin/bookings">Bookings</router-link>
      <router-link to="/admin/search">Search</router-link>
    </div>

    <div v-if="role === 'trekker'" class="nav-links">
      <router-link to="/trekker/dashboard">Dashboard</router-link>
      <router-link to="/trekker/treks">Browse Treks</router-link>
      <router-link to="/trekker/bookings">My Bookings</router-link>
      <router-link to="/trekker/profile">Profile</router-link>
    </div>

    <div v-if="role === 'staff'" class="nav-links">
      <router-link to="/staff/dashboard">Dashboard</router-link>
      <router-link to="/staff/treks">My Treks</router-link>
    </div>

    <div v-if="isLoggedIn" class="right-nav">
      <span class="user-greeting">Hey {{ username }}</span>
      <button @click="logout" class="btn-logout">Logout</button>
    </div>

    <div v-else class="right-nav">
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Register</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',

  computed: {
    role() {
      return localStorage.getItem('role') || ''
    },

    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
    username() {
      return localStorage.getItem('full_name') || 'User'
    },

    showNav() {
      const hideOn = ['Login', 'Register', 'Home']
      return !hideOn.includes(this.$route.name)
    },
  },

  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('full_name')
      this.$router.push('/login')
    },
    goHome() {
      const roleRoutes = {
        admin: '/admin/dashboard',
        staff: '/staff/dashboard',
        trekker: '/trekker/dashboard',
      }
      const destination = roleRoutes[this.role] || '/'
      this.$router.push(destination)
    },
  },
}
</script>

<style scoped>
nav {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 24px;
  padding: 14px 24px;
  background-color: #2c3e50;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
  cursor: pointer;
  margin-right: 12px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.right-nav {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-greeting {
  font-size: 0.92rem;
  color: #ecf0f1;
}

nav a {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 0.95rem;
  padding: 4px 0;
  transition: color 0.2s, border-color 0.2s;
}

nav a:hover {
  color: #f39c12;
}

nav a.router-link-active {
  color: #f39c12;
  font-weight: bold;
  border-bottom: 2px solid #f39c12;
}

.btn-logout {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 14px;
  cursor: pointer;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-logout:hover {
  background: #c0392b;
}
</style>
