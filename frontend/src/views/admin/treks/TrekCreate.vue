<template>
  <div class="page">

    <button class="btn-back" @click="$router.push('/admin/treks')">
      ← Back to Treks
    </button>

    <div class="card">
      <h1>Create New Trek</h1>
      <p class="subtitle">Fill in the details for the new trek</p>

      <form @submit.prevent="createTrek">

        <div class="form-row">
          <div class="form-group">
            <label>Trek Name *</label>
            <input v-model="form.trek_name" type="text" placeholder="e.g. Valley of Flowers" required />
          </div>
          <div class="form-group">
            <label>Location *</label>
            <input v-model="form.trek_location" type="text" placeholder="e.g. Uttarakhand, India" required />
          </div>
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea v-model="form.description" rows="4" placeholder="Brief overview of the trek..."></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Difficulty *</label>
            <select v-model="form.difficulty" required>
              <option value="" disabled>Select difficulty</option>
              <option value="easy">Easy</option>
              <option value="moderate">Moderate</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <div class="form-group">
            <label>Total Slots *</label>
            <input v-model.number="form.total_slot" type="number" min="1" placeholder="e.g. 20" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Start Date *</label>
            <input v-model="form.start_date" type="date" required />
          </div>
          <div class="form-group">
            <label>End Date *</label>
            <input v-model="form.end_date" type="date" required />
          </div>
        </div>

        <p v-if="durationText" class="duration-hint">{{ durationText }}</p>

        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Trek' }}
          </button>
          <button type="button" class="btn-secondary" @click="$router.push('/admin/treks')">
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
  name: 'TrekCreate',

  data() {
    return {
      form: {
        trek_name: '',
        trek_location: '',
        description: '',
        difficulty: '',
        total_slot: '',
        start_date: '',
        end_date: '',
      },
      loading: false,
      error: '',
      successMsg: '',
    }
  },

  computed: {
    durationText() {
      if (!this.form.start_date || !this.form.end_date) return ''
      const start = new Date(this.form.start_date)
      const end = new Date(this.form.end_date)
      const days = Math.round((end - start) / (1000 * 60 * 60 * 24))
      if (days <= 0) return '⚠️ End date must be after start date'
      return `📅 Duration: ${days} day${days > 1 ? 's' : ''}`
    },
  },

  methods: {
    async createTrek() {
      this.error = ''
      this.successMsg = ''

      if (new Date(this.form.end_date) <= new Date(this.form.start_date)) {
        this.error = 'End date must be after start date'
        return
      }

      this.loading = true
      try {
        const res = await api.post('/admin/trek_list', this.form)
        this.successMsg = `Trek created! (ID: ${res.data.id})`
        setTimeout(() => this.$router.push('/admin/treks'), 1500)
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to create trek'
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
  max-width: 760px;
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

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #2c3e50;
  box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.1);
}

.duration-hint {
  font-size: 0.9rem;
  color: #2c3e50;
  background: #eaf0fb;
  padding: 8px 14px;
  border-radius: 6px;
  margin-bottom: 12px;
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
