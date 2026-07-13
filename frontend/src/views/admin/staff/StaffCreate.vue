<template>
  <div class="page">

    <button class="btn-back" @click="$router.push('/admin/staff')">
      ← Back to Staff List
    </button>

    <div class="card">
      <h1>Add New Staff Member</h1>
      <p class="subtitle">Staff members can manage and lead treks</p>

      <form @submit.prevent="createStaff">

        <div class="form-row">
          <div class="form-group">
            <label>Full Name *</label>
            <input v-model="form.full_name" type="text" placeholder="e.g. John Doe" required />
          </div>
          <div class="form-group">
            <label>Email *</label>
            <input v-model="form.email" type="email" placeholder="e.g. john@example.com" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Password *</label>
            <input v-model="form.password" type="password" placeholder="Minimum 6 characters" required />
          </div>
          <div class="form-group">
            <label>Mobile Number *</label>
            <input v-model="form.mobile_no" type="text" placeholder="e.g. 9876543210" required />
          </div>
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Staff Member' }}
          </button>
          <button type="button" class="btn-secondary" @click="$router.push('/admin/staff')">
            Cancel
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import api from '../../../api'

export default {
  name: 'StaffCreate',

  data() {
    return {
      form: {
        full_name: '',
        email: '',
        password: '',
        mobile_no: '',
      },
      loading: false,
      error: '',
      successMsg: '',
    }
  },

  methods: {
    async createStaff() {
      this.error = ''
      this.successMsg = ''

      if (this.form.password.length < 6) {
        this.error = 'Password must be at least 6 characters'
        return
      }

      this.loading = true
      try {
        const res = await api.post('/admin/staff_list', this.form)
        this.successMsg = `Staff member created! (ID: ${res.data.id})`
        setTimeout(() => this.$router.push('/admin/staff'), 1500)
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to create staff'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.page {
  padding: 20px 0;
}

.btn-back {
  background: none;
  border: none;
  color: #2c3e50;
  cursor: pointer;
  font-size: 0.95rem;
  padding: 0;
  margin-bottom: 20px;
  display: block;
}

.btn-back:hover {
  text-decoration: underline;
}

.card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 30px;
  max-width: 700px;
}

.card h1 {
  font-size: 1.4rem;
  color: #2c3e50;
  margin-bottom: 6px;
}

.subtitle {
  color: #7f8c8d;
  margin-bottom: 28px;
  font-size: 0.9rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 6px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #2c3e50;
  box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.btn-primary {
  background: #2c3e50;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #34495e;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #555;
  border: 1px solid #ddd;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}

.btn-secondary:hover {
  background: #f5f5f5;
}

.error-msg {
  color: #e74c3c;
  background: #fdf0f0;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
  margin-bottom: 12px;
}

.success-msg {
  color: #155724;
  background: #d4edda;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #28a745;
  margin-bottom: 12px;
}
</style>
