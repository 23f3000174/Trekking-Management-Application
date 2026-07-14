<template>
    <nav v-if="showNav">
        <span @click="goHome" style="cursor:pointer; font-weight:bold;">
            TrekkingApp
        </span>

        <span v-if="role === 'admin'">
            <router-link to="/admin/dashboard">Dashboard</router-link>
            <router-link to="/admin/staff">Staff</router-link>
            <router-link to="/admin/treks">Treks</router-link>
            <router-link to="/admin/trekkers">Trekkers</router-link>
            <router-link to="/admin/bookings">Bookings</router-link>
            <router-link to="/admin/search">Search</router-link>
        </span>

        <span v-if="role === 'staff'">
            <router-link to="/staff/dashboard">Dashboard</router-link>
            <router-link to="/staff/treks">My Treks</router-link>
        </span>

        <span v-if="isLoggedIn" style="float:right;">
            <span>{{ username }}</span>
            <button @click="logout">Logout</button>
        </span>

        <span v-else style="float:right;">
            <router-link to="/login">Login</router-link>
            <router-link to="/register">Register</router-link>
        </span>
    </nav>
</template>

<script>
export default{
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
                admin : '/admin/dashboard',
                staff : '/staff/dashboard',
                trekker: 'trekker/dashboard',
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
  gap: 16px;
  padding: 10px 20px;
  background-color: #2c3e50;
  color: white;
}

nav a {
  color: #ecf0f1;
  text-decoration: none;
}

nav a.router-link-active {
  color: #f39c12;
  font-weight: bold;
  border-bottom: 2px solid #f39c12;
}

nav button {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 4px 12px;
  cursor: pointer;
  border-radius: 4px;
}
</style>
