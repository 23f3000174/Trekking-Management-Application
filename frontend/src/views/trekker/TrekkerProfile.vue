<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1>My Profile</h1>
        <p class="subtitle">View and update your personal details</p>
      </div>
      <button class="btn-secondary" @click="$router.push('/trekker/dashboard')">
        ← Dashboard
      </button>
    </div>

    <div v-if="loading" class="loading">Loading profile...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="content">
      <div class="card">
        <form @submit.prevent="updateProfile">
          <div class="form-grid">
            <div class="form-group">
              <label>Full Name</label>
              <input v-model="form.full_name" type="text" required />
            </div>

            <div class="form-group">
              <label>Email Address</label>
              <input :value="form.email" type="email" disabled class="disabled-input" />
              <small class="help-text">Email cannot be changed</small>
            </div>

            <div class="form-group">
              <label>Mobile Number</label>
              <input v-model="form.mobile_no" type="text" required />
            </div>

            <div class="form-group">
              <label>Date of Birth</label>
              <input v-model="form.dob" type="date" required />
            </div>

            <div class="form-group">
              <label>Gender</label>
              <select v-model="form.gender" required>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="prefer not to say">Prefer not to say</option>
              </select>
            </div>

            <div class="form-group">
              <label>Emergency Contact</label>
              <input v-model="form.emergency_contact" type="text" />
            </div>
            
            <div class="form-group">
              <label>Account Status</label>
              <p class="status-field">
                <span class="badge" :class="'badge-' + form.flag">{{ form.flag }}</span>
              </p>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="actionLoading">
              {{ actionLoading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>

        <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>
        <p v-if="actionError" class="error-msg">{{ actionError }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'TrekkerProfile',

  data() {
    return {
      form: {
        full_name: '',
        email: '',
        mobile_no: '',
        dob: '',
        gender: '',
        emergency_contact: '',
        flag: ''
      },
      loading: true,
      error: '',
      actionLoading: false,
      successMsg: '',
      actionError: '',
    }
  },

  async mounted() {
    await this.fetchProfile()
  },

  methods: {
    async fetchProfile() {
      this.loading = true
      this.error = ''
      try {
        const res = await api.get('/trekker/profile')
        this.form = { ...res.data }
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to load profile details'
      } finally {
        this.loading = false
      }
    },

    async updateProfile() {
      this.actionLoading = true
      this.successMsg = ''
      this.actionError = ''
      
      const payload = {
        full_name: this.form.full_name,
        mobile_no: this.form.mobile_no,
        dob: this.form.dob,
        gender: this.form.gender,
        emergency_contact: this.form.emergency_contact
      }

      try {
        const res = await api.put('/trekker/profile', payload)
        this.successMsg = res.data.message || 'Profile updated successfully!'
        
        // Update user name in local storage in case it changed
        localStorage.setItem('full_name', this.form.full_name)
        
        setTimeout(() => { this.successMsg = '' }, 3000)
      } catch (e) {
        this.actionError = e.response?.data?.message || 'Failed to update profile'
      } finally {
        this.actionLoading = false
      }
    }
  }
}
</script>

<style scoped>
.page {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 12px;
}

.page-header h1 {
  font-size: 1.6rem;
  color: #2c3e50;
  margin: 0;
}

.subtitle {
  color: #7f8c8d;
  margin-top: 4px;
  font-size: 0.9rem;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 6px;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #2c3e50;
}

.disabled-input {
  background-color: #f8f9fa;
  color: #7f8c8d;
  cursor: not-allowed;
  border-color: #e0e0e0;
}

.help-text {
  font-size: 0.75rem;
  color: #7f8c8d;
  margin-top: 4px;
}

.status-field {
  margin: 6px 0 0 0;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: capitalize;
}

.badge-active {
  background: #d4edda;
  color: #155724;
}

.badge-inactive {
  background: #fff3cd;
  color: #856404;
}

.badge-blacklisted {
  background: #f8d7da;
  color: #721c24;
}

.form-actions {
  display: flex;
  justify-content: flex-start;
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
}

.btn-primary {
  background: #2c3e50;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #34495e;
}

.btn-secondary {
  background: white;
  color: #2c3e50;
  border: 1px solid #2c3e50;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-msg {
  color: #155724;
  background: #d4edda;
  padding: 8px 14px;
  border-radius: 6px;
  margin-top: 16px;
}

.error-msg {
  color: #e74c3c;
  background: #fdf0f0;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
  margin-top: 16px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}
</style>
