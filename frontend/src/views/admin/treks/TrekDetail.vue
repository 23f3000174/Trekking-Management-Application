<template>
  <div class="page">

    <button class="btn-back" @click="$router.push('/admin/treks')">
      ← Back to Treks
    </button>

    <div v-if="loading" class="loading">Loading trek details...</div>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="content">

      <div class="card">
        <div class="trek-header">
          <div>
            <h2>{{ trek.trek_name }}</h2>
            <p class="location">📍 {{ trek.trek_location }}</p>
          </div>
          <span class="badge" :class="{
            'badge-pending': trek.trek_status === 'pending',
            'badge-approved': trek.trek_status === 'approved',
            'badge-open': trek.trek_status === 'open',
            'badge-closed': trek.trek_status === 'closed',
            'badge-completed': trek.trek_status === 'completed'
          }">
            {{ trek.trek_status }}
          </span>
        </div>

        <p v-if="trek.description" class="description">{{ trek.description }}</p>

        <div class="info-grid">
          <div class="info-item">
            <label>Difficulty</label>
            <p class="capitalize">{{ trek.difficulty }}</p>
          </div>
          <div class="info-item">
            <label>Duration</label>
            <p>{{ trek.duration_days }} days</p>
          </div>
          <div class="info-item">
            <label>Start Date</label>
            <p>{{ formatDate(trek.start_date) }}</p>
          </div>
          <div class="info-item">
            <label>End Date</label>
            <p>{{ formatDate(trek.end_date) }}</p>
          </div>
          <div class="info-item">
            <label>Total Slots</label>
            <p>{{ trek.total_slot }}</p>
          </div>
          <div class="info-item">
            <label>Available Slots</label>
            <p>{{ trek.available_slot }}</p>
          </div>
        </div>

        <div class="info-item staff-section">
          <label>Assigned Staff</label>
          <p v-if="!trek.assigned_staff">Not assigned yet</p>
          <p v-else class="link" @click="$router.push(`/admin/staff/${trek.assigned_staff.id}`)">
            {{ trek.assigned_staff.full_name }} — {{ trek.assigned_staff.email }}
          </p>
        </div>

        <div class="card-actions">
          <button class="btn-secondary" @click="showEditForm = !showEditForm">
            {{ showEditForm ? 'Cancel Edit' : '✏️ Edit' }}
          </button>
          <button class="btn-danger" @click="deleteTrek" :disabled="actionLoading">
            🗑️ Delete
          </button>
        </div>
      </div>

      <div v-show="showEditForm" class="card edit-card">
        <h3>Edit Trek</h3>

        <div class="form-row">
          <div class="form-group">
            <label>Trek Name</label>
            <input v-model="editForm.trek_name" type="text" />
          </div>
          <div class="form-group">
            <label>Location</label>
            <input v-model="editForm.trek_location" type="text" />
          </div>
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea v-model="editForm.description" rows="3"></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Difficulty</label>
            <select v-model="editForm.difficulty">
              <option value="easy">Easy</option>
              <option value="moderate">Moderate</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="editForm.trek_status">
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="open">Open</option>
              <option value="closed">Closed</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Total Slots</label>
            <input v-model.number="editForm.total_slot" type="number" min="1" />
          </div>
          <div class="form-group">
            <label>Assign Staff ID</label>
            <input v-model.number="editForm.assigned_staff_id" type="number" placeholder="Leave empty to unassign" />
          </div>
        </div>

        <p v-if="updateMsg" class="success-msg">{{ updateMsg }}</p>

        <button class="btn-primary" @click="updateTrek" :disabled="actionLoading">
          Save Changes
        </button>
      </div>

    </div>
  </div>
</template>

<script>
import api from '../../../api'

export default {
  name: 'TrekDetail',

  data() {
    return {
      trek: {},
      loading: true,
      error: '',
      showEditForm: false,
      actionLoading: false,
      updateMsg: '',
      editForm: {
        trek_name: '',
        trek_location: '',
        description: '',
        difficulty: '',
        trek_status: '',
        total_slot: 0,
        assigned_staff_id: null,
      },
    }
  },

  async mounted() {
    const id = this.$route.params.id
    try {
      const res = await api.get(`/admin/trek/${id}`)
      this.trek = res.data
      this.editForm = {
        trek_name: this.trek.trek_name,
        trek_location: this.trek.trek_location,
        description: this.trek.description,
        difficulty: this.trek.difficulty,
        trek_status: this.trek.trek_status,
        total_slot: this.trek.total_slot,
        assigned_staff_id: this.trek.assigned_staff?.id || null,
      }
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load trek'
    } finally {
      this.loading = false
    }
  },

  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '—'
      return new Date(dateStr).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    },

    async updateTrek() {
      this.actionLoading = true
      try {
        await api.put(`/admin/trek/${this.trek.id}`, this.editForm)
        this.trek.trek_name = this.editForm.trek_name
        this.trek.trek_status = this.editForm.trek_status
        this.updateMsg = 'Trek updated successfully!'
        setTimeout(() => {
          this.updateMsg = ''
          this.showEditForm = false
        }, 1500)
      } catch (e) {
        this.error = e.response?.data?.message || 'Update failed'
      } finally {
        this.actionLoading = false
      }
    },

    async deleteTrek() {
      if (!confirm(`Delete "${this.trek.trek_name}"? This cannot be undone.`)) return
      this.actionLoading = true
      try {
        await api.delete(`/admin/trek/${this.trek.id}`)
        this.$router.push('/admin/treks')
      } catch (e) {
        this.error = e.response?.data?.message || 'Delete failed'
        this.actionLoading = false
      }
    },
  },
}
</script>

<style scoped>
.page {
  padding: 20px 0;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  padding: 24px;
}

.card h3 {
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}

.edit-card {
  border-left: 4px solid #3498db;
}

.trek-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 16px;
}

.trek-header h2 {
  font-size: 1.4rem;
  color: #2c3e50;
}

.location {
  color: #7f8c8d;
  margin-top: 4px;
  font-size: 0.9rem;
}

.description {
  color: #555;
  margin-bottom: 20px;
  line-height: 1.6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 14px;
}

.info-item label {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7f8c8d;
  display: block;
  margin-bottom: 4px;
}

.info-item p {
  font-size: 0.95rem;
  color: #2c3e50;
}

.capitalize {
  text-transform: capitalize;
}

.staff-section {
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  margin-bottom: 16px;
}

.link {
  color: #2980b9;
  cursor: pointer;
  text-decoration: underline;
}

.card-actions {
  display: flex;
  gap: 10px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  flex-wrap: wrap;
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
  margin-bottom: 16px;
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
  padding: 8px 12px;
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
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.82rem;
  font-weight: 600;
  text-transform: capitalize;
  flex-shrink: 0;
}

.badge-pending {
  background: #fff3cd;
  color: #856404;
}

.badge-approved {
  background: #cce5ff;
  color: #004085;
}

.badge-open {
  background: #d4edda;
  color: #155724;
}

.badge-closed {
  background: #f8d7da;
  color: #721c24;
}

.badge-completed {
  background: #e2e3e5;
  color: #383d41;
}

.btn-primary {
  background: #2c3e50;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #34495e;
}

.btn-secondary {
  background: white;
  color: #2c3e50;
  border: 1px solid #2c3e50;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-danger {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 9px 18px;
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
  margin-bottom: 12px;
}

.error-msg {
  color: #e74c3c;
  background: #fdf0f0;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}
</style>
