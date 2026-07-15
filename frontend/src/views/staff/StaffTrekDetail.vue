<template>
  <div class="page">

    <button class="btn-back" @click="$router.push('/staff/treks')">
      ← Back to My Treks
    </button>

    <div v-if="loading" class="loading">Loading trek details...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

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
            <label>Booked</label>
            <p>{{ trek.booked_count }}</p>
          </div>
          <div class="info-item">
            <label>Available Slots</label>
            <p>{{ trek.available_slot }} / {{ trek.total_slot }}</p>
          </div>
        </div>

        <div class="card-actions">
          <button class="btn-secondary" @click="showEditForm = !showEditForm">
            {{ showEditForm ? 'Cancel Edit' : '✏️ Edit Trek' }}
          </button>
        </div>
      </div>

      <div v-show="showEditForm" class="card edit-card">
        <h3>Update Trek</h3>

        <div class="form-group">
          <label>Description</label>
          <textarea v-model="editForm.description" rows="3"></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Total Slots</label>
            <input v-model.number="editForm.total_slot" type="number" min="0" />
            <small class="hint">Cannot be less than currently booked ({{ trek.booked_count }}).</small>
          </div>
          <div class="form-group">
            <label>Trek Status</label>
            <select v-model="editForm.trek_status">
              <option value="approved">Approved</option>
              <option value="open">Open</option>
              <option value="closed">Closed</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>

        <p v-if="updateMsg" class="success-msg">{{ updateMsg }}</p>
        <p v-if="updateError" class="error-msg">{{ updateError }}</p>

        <button class="btn-primary" @click="updateTrek" :disabled="actionLoading">
          Save Changes
        </button>
      </div>

      <div class="card">
        <div class="card-title-row">
          <h3>Registered Trekkers</h3>
          <span class="count-badge">{{ participants.length }} total</span>
        </div>

        <div v-if="participants.length === 0" class="empty">
          No trekkers registered for this trek yet.
        </div>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Trekker</th>
              <th>Email</th>
              <th>Mobile</th>
              <th>Booked On</th>
              <th>Booking Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in participants" :key="p.booking_id">
              <td>{{ p.user_id }}</td>
              <td>{{ p.full_name }}</td>
              <td>{{ p.email }}</td>
              <td>{{ p.mobile_no || '—' }}</td>
              <td>{{ formatDate(p.booking_date) }}</td>
              <td>
                <span class="badge" :class="{
                  'badge-booked': p.booking_status === 'booked',
                  'badge-cancelled': p.booking_status === 'cancelled',
                  'badge-completed': p.booking_status === 'completed'
                }">
                  {{ p.booking_status }}
                </span>
              </td>
              <td>
                <span v-if="p.booking_status === 'cancelled' && p.cancelled_by === 'trekker'" class="text-muted">
                  Cancelled by trekker
                </span>
                <span v-else-if="p.booking_status === 'completed'" class="text-muted">
                  —
                </span>
                <div v-else-if="p.booking_status === 'booked'" class="action-buttons-inline">
                  <button 
                    class="btn-success-sm" 
                    @click="updateBookingStatus(p, 'completed')"
                    :disabled="statusLoading === p.booking_id"
                  >
                    Complete
                  </button>
                  <button 
                    class="btn-danger-sm" 
                    @click="updateBookingStatus(p, 'cancelled')"
                    :disabled="statusLoading === p.booking_id"
                  >
                    Cancel
                  </button>
                </div>
                <div v-else-if="p.booking_status === 'cancelled'" class="action-buttons-inline">
                  <button 
                    class="btn-success-sm" 
                    @click="updateBookingStatus(p, 'booked')"
                    :disabled="statusLoading === p.booking_id"
                  >
                    Rebook
                  </button>
                  <span class="text-muted"> (Cancelled by {{ p.cancelled_by || 'staff' }})</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'StaffTrekDetail',

  data() {
    return {
      trek: {},
      participants: [],
      loading: true,
      error: '',
      showEditForm: false,
      actionLoading: false,
      updateMsg: '',
      updateError: '',
      statusLoading: null,
      statusDrafts: {},
      editForm: {
        description: '',
        total_slot: 0,
        trek_status: '',
      },
    }
  },

  async mounted() {
    const id = this.$route.params.id
    try {
      const res = await api.get(`/staff/treks/${id}`)
      this.trek = res.data
      this.participants = res.data.participants || []
      this.editForm = {
        description: this.trek.description || '',
        total_slot: this.trek.total_slot,
        trek_status: this.trek.trek_status,
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
      this.updateMsg = ''
      this.updateError = ''
      const payload = {
        description: this.editForm.description,
        total_slot: this.editForm.total_slot,
        trek_status: this.editForm.trek_status,
      }
      try {
        const res = await api.put(`/staff/treks/${this.trek.id}`, payload)
        this.trek.trek_status = res.data.trek_status
        this.trek.total_slot = res.data.total_slot
        this.trek.available_slot = res.data.available_slot
        this.updateMsg = 'Trek updated successfully!'
        setTimeout(() => {
          this.updateMsg = ''
          this.showEditForm = false
        }, 1500)
      } catch (e) {
        this.updateError = e.response?.data?.message || 'Update failed'
      } finally {
        this.actionLoading = false
      }
    },

    async updateBookingStatus(participant, newStatus) {
      this.statusLoading = participant.booking_id
      try {
        const res = await api.put(`/staff/bookings/${participant.booking_id}`, {
          booking_status: newStatus,
        })
        participant.booking_status = res.data.booking_status
        participant.cancelled_by = res.data.cancelled_by
        if (res.data.available_slot !== undefined) {
          this.trek.available_slot = res.data.available_slot
        }
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to update booking status'
        setTimeout(() => { this.error = '' }, 3000)
      } finally {
        this.statusLoading = null
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

.card-actions {
  display: flex;
  gap: 10px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.card-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.card-title-row h3 {
  margin: 0;
  border: none;
  padding: 0;
}

.count-badge {
  background: #eef2f7;
  color: #2c3e50;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.82rem;
  font-weight: 600;
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

.hint {
  display: block;
  color: #95a5a6;
  font-size: 0.78rem;
  margin-top: 4px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 8px 12px;
  font-size: 0.82rem;
  text-transform: uppercase;
  color: #7f8c8d;
  border-bottom: 2px solid #f0f0f0;
}

.data-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #f8f8f8;
  font-size: 0.9rem;
}

.status-select {
  padding: 5px 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.82rem;
  background: white;
  cursor: pointer;
}

.status-select:focus {
  outline: none;
  border-color: #2c3e50;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78rem;
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

.badge-booked {
  background: #cce5ff;
  color: #004085;
}

.badge-cancelled {
  background: #f8d7da;
  color: #721c24;
}

.badge-completed {
  background: #d4edda;
  color: #155724;
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
  margin-bottom: 12px;
}

.empty {
  color: #7f8c8d;
  font-size: 0.95rem;
  padding: 20px 0;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.action-buttons-inline {
  display: flex;
  gap: 8px;
}

.btn-success-sm {
  background: #2ecc71;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-success-sm:hover {
  background: #27ae60;
}

.btn-danger-sm {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-danger-sm:hover {
  background: #c0392b;
}

.text-muted {
  color: #7f8c8d;
  font-size: 0.9rem;
  font-style: italic;
}
</style>
