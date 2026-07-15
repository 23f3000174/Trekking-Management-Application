<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Login</h1>
      <p class="subtitle">Log in to manage or book treks</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email:</label>
          <input type="email" v-model="form.email" placeholder="Enter your email" required />
        </div>

        <div class="form-group">
          <label>Password:</label>
          <input type="password" v-model="form.password" placeholder="Enter your password" required />
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Login....' : 'Login' }}
        </button>
      </form>

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <p class="auth-footer">
        Created a new Account? <router-link to="/register">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API = "http://localhost:5000/api/auth"
export default {
  name : 'LoginView',

  data() {
    return{
      form: {
        email: '',
        password: '',
      },
      errorMsg: '',
      loading: false
    }
  },

  methods: {
    async handleLogin() {
      this.loading = true
      this.errorMsg = ''

      try {
        const response = await axios.post(`${API}/login`, this.form)
        const { access_token , role } = response.data

        localStorage.setItem('token', access_token)
        localStorage.setItem('role', role)
        localStorage.setItem('full_name', response.data.full_name)

        if (role === 'admin') {
          this.$router.push('/admin/dashboard')
        } else if (role === 'staff') {
          this.$router.push('/staff/dashboard')
        } else {
          this.$router.push('/trekker/dashboard')
        }

      } catch (error){
        this.errorMsg = error.response?.data?.message || 'Login failed'
      } finally {
        this.loading = false
      }
    }
  },
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  padding: 20px;
  background-color: #f8f9fa;
}

.auth-card {
  width: 100%;
  max-width: 450px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.auth-card h1 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 8px;
  text-align: center;
}

.subtitle {
  color: #7f8c8d;
  font-size: 0.92rem;
  text-align: center;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #2c3e50;
  outline: none;
}

.btn-primary {
  width: 100%;
  background: #2c3e50;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #34495e;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-msg {
  color: #e74c3c;
  background: #fdf0f0;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
  margin-top: 16px;
  font-size: 0.9rem;
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.auth-footer a {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
