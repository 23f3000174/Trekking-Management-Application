<template>
  <div class="page">
    <button class="btn-back" @click="$router.push('/trekker/bookings')">
      ← Back to Bookings
    </button>

    <div v-if="loading" class="loading">Loading booking details...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="content">
      <div class="card">
        <div class="booking-header">
          <div>
            <h2>Booking #{{ booking.booking_id }}</h2>
            <p class="trek-title">🏔️ {{ booking.trek.trek_name }}</p>
            <p class="location">📍 {{ booking.trek.trek_location }}</p>
          </div>
          <span class="badge" :class="'badge-' + booking.booking_status">
            {{ booking.booking_status }}
          </span>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <label>Booked On</label>
            <p>{{ formatDate(booking.booking_date) }}</p>
          </div>
          <div class="info-item" v-if="booking.cancellation_date">
            <label>Cancelled On</label>
            <p class="cancelled-text">{{ formatDate(booking.cancellation_date) }}</p>
          </div>
          <div class="info-item">
            <label>Start Date</label>
            <p>{{ formatDate(booking.trek.start_date) }}</p>
          </div>
          <div class="info-item">
            <label>End Date</label>
            <p>{{ formatDate(booking.trek.end_date) }}</p>
          </div>
          <div class="info-item">
            <label>Difficulty</label>
            <p class="capitalize">{{ booking.trek.difficulty }}</p>
          </div>
          <div class="info-item">
            <label>Trek Status</label>
            <p><span class="badge" :class="'badge-' + booking.trek.trek_status">{{ booking.trek.trek_status }}</span>
            </p>
          </div>
        </div>

        <div class="card-actions">
          <button
            v-if="booking.booking_status === 'booked' && booking.trek.trek_status !== 'completed' && booking.trek.trek_status !== 'closed'"
            class="btn-danger" @click="cancelBooking" :disabled="actionLoading">
            {{ actionLoading ? 'Cancelling...' : 'Cancel Booking' }}
          </button>

          <button v-if="booking.booking_status === 'cancelled'" class="btn-danger-outline" @click="deleteBooking"
            :disabled="actionLoading">
            {{ actionLoading ? 'Deleting...' : 'Delete Booking Record' }}
          </button>
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
  name: 'TrekkerBookingDetail',

  data() {
    return {
      booking: {},
      loading: true,
      error: '',
      actionLoading: false,
      actionMsg: '',
      actionError: '',
    }
  },

  async mounted() {
    await this.fetchBookingDetails()
  },

  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '—'
      return new Date(dateStr).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    async fetchBookingDetails() {
      const id = this.$route.params.id
      this.loading = true
      this.error = ''
      try {
        const res = await api.get(`/trekker/bookings/${id}`)
        console.log(res.data)
        this.booking = res.data
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to load booking details'
      } finally {
        this.loading = false
      }
    },

    async cancelBooking() {
      if (!confirm('Are you sure you want to cancel this booking?')) return
      this.actionLoading = true
      this.actionMsg = ''
      this.actionError = ''
      try {
        const res = await api.put(`/trekker/bookings/${this.booking.booking_id}`, {
          booking_status: 'cancelled'
        })
        this.actionMsg = res.data.message
        this.booking.booking_status = res.data.booking_status
        this.booking.cancellation_date = new Date().toISOString()
        if (this.booking.trek) {
          this.booking.trek.available_slot = res.data.available_slot
        }
      } catch (e) {
        this.actionError = e.response?.data?.message || 'Cancellation failed'
      } finally {
        this.actionLoading = false
      }
    },

    async deleteBooking() {
      if (!confirm('Are you sure you want to permanently delete this booking record?')) return
      this.actionLoading = true
      this.actionMsg = ''
      this.actionError = ''
      try {
        await api.delete(`/trekker/bookings/${this.booking.booking_id}`)
        this.$router.push('/trekker/bookings')
      } catch (e) {
        this.actionError = e.response?.data?.message || 'Deletion failed'
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

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 16px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 16px;
}

.booking-header h2 {
  font-size: 1.4rem;
  color: #2c3e50;
  margin: 0;
}

.trek-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #34495e;
  margin: 6px 0 2px 0;
}

.location {
  color: #7f8c8d;
  margin: 0;
  font-size: 0.9rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.info-item {
  margin-bottom: 10px;
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
  margin: 0;
}

.cancelled-text {
  color: #e74c3c !important;
  font-weight: 500;
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
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: capitalize;
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

.badge-open {
  background: #d4edda;
  color: #155724;
}

.badge-pending {
  background: #fff3cd;
  color: #856404;
}

.badge-approved {
  background: #cce5ff;
  color: #004085;
}

.badge-closed {
  background: #f8d7da;
  color: #721c24;
}

.btn-danger {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.btn-danger:hover {
  background: #c0392b;
}

.btn-danger-outline {
  background: white;
  color: #e74c3c;
  border: 1px solid #e74c3c;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s, color 0.2s;
}

.btn-danger-outline:hover {
  background: #e74c3c;
  color: white;
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
