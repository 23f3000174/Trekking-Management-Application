<template>
  <div class="page">

    <button class="btn-back" @click="$router.push('/trekker/treks')">
      ← Back to Treks
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
          <span class="badge" :class="'badge-' + trek.trek_status">
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
            <label>Available Slots</label>
            <p>{{ trek.available_slot }} / {{ trek.total_slot }}</p>
          </div>
          <div class="info-item">
            <label>Assigned Staff</label>
            <p v-if="!trek.assigned_staff">Not assigned yet</p>
            <p v-else>{{ trek.assigned_staff.full_name }} — {{ trek.assigned_staff.email }}</p>
          </div>
        </div>

        <div class="card-actions">
          <p v-if="trek.my_booking" class="already-booked">
            Your booking status:
            <span class="badge" :class="'badge-' + trek.my_booking">{{ trek.my_booking }}</span>
          </p>

          <button
            v-else-if="trek.trek_status === 'open' && trek.available_slot > 0"
            class="btn-primary"
            @click="bookTrek"
            :disabled="actionLoading"
          >
            {{ actionLoading ? 'Booking...' : 'Book This Trek' }}
          </button>

          <p v-else-if="trek.my_booking === null && trek.trek_status !== 'open'" class="hint">
            This trek is not currently open for booking.
          </p>
          <p v-else-if="trek.available_slot <= 0" class="hint">
            Sorry, this trek is fully booked.
          </p>
        </div>

        <p v-if="actionMsg" class="success-msg">{{ actionMsg }}</p>
        <p v-if="actionError" class="error-msg">{{ actionError }}</p>
      </div>

    </div>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'TrekkerTrekDetail',

  data() {
    return {
      trek: {},
      loading: true,
      error: '',
      actionLoading: false,
      actionMsg: '',
      actionError: '',
    }
  },

  async mounted() {
    const id = this.$route.params.id
    try {
      const res = await api.get(`/trekker/treks/${id}`)
      this.trek = res.data
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

    async bookTrek() {
      this.actionLoading = true
      this.actionMsg = ''
      this.actionError = ''
      try {
        const res = await api.post(`/trekker/bookings/${this.trek.id}`)
        this.actionMsg = res.data.message
        this.trek.my_booking = res.data.booking_status
        this.trek.available_slot = res.data.available_slot
        setTimeout(() => { this.actionMsg = '' }, 2500)
      } catch (e) {
        this.actionError = e.response?.data?.message || 'Booking failed'
      } finally {
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
  align-items: center;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.already-booked {
  color: #2c3e50;
  font-size: 0.92rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.hint {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0;
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
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #34495e;
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
  margin-top: 12px;
}

.error-msg {
  color: #e74c3c;
  background: #fdf0f0;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
  margin-top: 12px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}
</style>
