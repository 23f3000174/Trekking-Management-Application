<template>
  <div>
   <h1>Login</h1>

   <form @submit.prevent="handleLogin">

     <div>
       <label>Email:</label>
       <input type="email" v-model="form.email" required />
     </div>

     <div>
       <label>Password:</label>
       <input type="password" v-model="form.password" required />
     </div>

     <button type="submit" :disabled="loading">
       {{ loading ? 'Login....' : 'Login' }}
       </button>
   </form>

   <p v-if="errorMsg" style="color:red"> {{ errorMsg }}</p>

   <p>Created a new Account? <a href="/register"> Register here</a></p>
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
