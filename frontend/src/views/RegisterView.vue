<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>Register</h1>
      <p class="subtitle">Create a trekker account to get started</p>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Full Name:</label>
          <input type="text" v-model="form.full_name" placeholder="Enter your full name" required />
        </div>

        <div class="form-group">
          <label>Email:</label>
          <input type="email" v-model="form.email" placeholder="Enter your email" required />
        </div>

        <div class="form-group">
          <label>Password:</label>
          <input type="password" v-model="form.password" placeholder="Choose a password" required />
        </div>

        <div class="form-group">
          <label>Mobile No:</label>
          <input type="text" v-model="form.mobile_no" placeholder="Enter your mobile number" required />
        </div>

        <div class="form-group">
          <label>Date of Birth:</label>
          <input type="date" v-model="form.dob" required />
        </div>

        <div class="form-group">
          <label>Gender:</label>
          <select v-model="form.gender" required>
            <option value="">__ Select __</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="prefer not to say">Prefer not to say</option>
          </select>
        </div>

        <div class="form-group">
          <label>Emergency Contact (optional):</label>
          <input type="text" v-model="form.emergency_contact" placeholder="Emergency contact number" />
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Register....' : 'Register' }}
        </button>
      </form>

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
      <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>

      <p class="auth-footer">
        Already have an account? <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const API = 'http://localhost:5000/api/auth'

export default {
  name: 'RegisterView',

  data() {
    return{
      form: {
        full_name: '',
        email: '',
        password: '',
        mobile_no: '',
        dob: '',
        gender: '',
        emergency_contact: ''
      },
      errorMsg: '',
      successMsg: '',
      loading: false
    }
  },

  methods: {
    async handleRegister() {
      this.loading = true
      this.errorMsg = ''
      this.successMsg = ''

      try {
        console.log(this.form)
        console.log('before api')
        await axios.post(`${API}/register`, this.form)
        console.log('after sending api')
        this.successMsg = 'Register successfully! Redirecting to login...'
        console.log('after this.succ')

        setTimeout(() => this.$router.push('/login'), 1500)

        console.log('after settimeout')
      } catch (error) {
        this.errorMsg = error.response?.data?.message || 'Register failed'
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
  max-width: 480px;
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
  margin-bottom: 18px;
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
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
  margin-top: 10px;
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

.success-msg {
  color: #155724;
  background: #d4edda;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #155724;
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
