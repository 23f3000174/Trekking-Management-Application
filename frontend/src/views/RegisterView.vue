<template>
  <div>
    <h1> Register </h1>

    <form @submit.prevent="handleRegister">

      <div>
        <label>Full Name:</label>
        <input type="text" v-model="form.full_name" required />
      </div>

      <div>
        <label>Email:</label>
        <input type="email" v-model="form.email" required />
      </div>

      <div>
        <label>Password:</label>
        <input type="password" v-model="form.password" required />
      </div>

      <div>
        <label>Mobile No:</label>
        <input type="text" v-model="form.mobile_no" required />
      </div>

      <div>
        <label>Date of Birth:</label>
        <input type="date" v-model="form.dob" required />
      </div>

      <div>
        <label>Gender:</label>
        <select v-model="form.gender" required>
          <option value="">__ Select __</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
          <option value="prefer not to say">Prefer not to say</option>
        </select>
      </div>

      <div>
        <label>Emergeny Contact (optional):</label>
        <input type="text" v-model="form.emergency_contact" />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Register....' : 'Register' }}
      </button>

    </form>

    <p v-if="errorMsg" style="color:red"> {{ errorMsg }}</p>
    <p v-if="successMsg" style="color:green"> {{ successMsg }}</p>

    <p>Already have an account? <a href="/login">Login here</a></p>
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
