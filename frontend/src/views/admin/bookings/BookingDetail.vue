<template>
  <div class="page">

    <button class="btn-back" @click="$router.push('/admin/bookings')">
      ← Back to Bookings
    </button>

    <div v-if="loading" class="loading">Loading booking...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="content">

      <div class="banner" :class="'banner-' + booking.booking_status">
        <div>
          <p class="banner-label">Booking #{{ booking.booking_id }}</p>
          <p class="banner-date">Booked on {{ formatDate(booking.booking_date) }}</p>
        </div>
        <span class="badge" :class="{
          'badge-booked': booking.booking_status === 'booked',
          'badge-cancelled': booking.booking_status === 'cancelled',
          'badge-completed': booking.booking_status === 'completed'
        }">
          {{ booking.booking_status }}
        </span>
      </div>

      <div v-if="booking.booking_status === 'cancelled'" class="cancel-notice">
        🚫 Cancelled on {{ formatDate(booking.cancellation_date) }}
      </div>

      <div class="two-col">

        <div class="card">
          <h3>👤 Trekker</h3>
          <div class="info-item">
            <label>Name</label>
            <p class="link" @click="$router.push(`/admin/trekkers/${booking.user?.id}`)">
              {{ booking.user?.full_name }}
            </p>
          </div>
          <div class="info-item">
            <label>Email</label>
            <p>{{ booking.user?.email }}</p>
          </div>
        </div>

        <div class="card">
          <h3>🏔️ Trek</h3>
          <div class="info-item">
            <label>Name</label>
            <p class="link" @click="$router.push(`/admin/treks/${booking.trek?.id}`)">
              {{ booking.trek?.trek_name }}
            </p>
          </div>
          <div class="info-item">
            <label>Location</label>
            <p>{{ booking.trek?.trek_location }}</p>
          </div>
          <div class="info-item">
            <label>Dates</label>
            <p>{{ formatDate(booking.trek?.start_date) }} → {{ formatDate(booking.trek?.end_date) }}</p>
          </div>
          <div class="info-item">
            <label>Trek Status</label>
            <span class="badge" :class="'badge-' + booking.trek?.trek_status">
              {{ booking.trek?.trek_status }}
            </span>
          </div>
        </div>

      </div>

      <div class="card actions-card">
        <h3>⚡ Booking Actions</h3>
        <div class="action-buttons">
          <button v-if="booking.booking_status === 'booked'" class="btn-danger" @click="updateBookingStatus('cancelled')" :disabled="actionLoading">
            Cancel Booking
          </button>
          <button v-if="booking.booking_status === 'booked'" class="btn-primary" @click="updateBookingStatus('completed')" :disabled="actionLoading">
            Mark Completed
          </button>
          <button v-if="booking.booking_status === 'cancelled'" class="btn-success" @click="updateBookingStatus('booked')" :disabled="actionLoading">
            Rebook Booking
          </button>
          <span v-if="actionLoading" class="loading-inline">Updating...</span>
        </div>
        <p v-if="actionSuccess" class="success-msg">{{ actionSuccess }}</p>
        <p v-if="actionError" class="error-msg">{{ actionError }}</p>
      </div>

    </div>
  </div>
</template>

<script>
import api from '../../../api'

export default {
  name: 'BookingDetail',

  data() {
    return {
      booking: {},
      loading: true,
      error: '',
      actionLoading: false,
      actionSuccess: '',
      actionError: '',
    }
  },

  async mounted() {
    const id = this.$route.params.id
    try {
      const res = await api.get(`/admin/bookings/${id}`)
      this.booking = res.data
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load booking'
    } finally {
      this.loading = false
    }
  },

  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '—'
      return new Date(dateStr).toLocaleDateString('en-IN', {
        year: 'numeric', month: 'short', day: 'numeric'
      })
    },

    async updateBookingStatus(newStatus) {
      this.actionLoading = true
      this.actionSuccess = ''
      this.actionError = ''
      try {
        const id = this.$route.params.id
        const res = await api.put(`/admin/bookings/${id}`, { booking_status: newStatus })
        this.actionSuccess = res.data.message
        this.booking.booking_status = res.data.booking_status
        if (res.data.available_slot !== undefined && this.booking.trek) {
          this.booking.trek.available_slot = res.data.available_slot
        }
        if (newStatus === 'cancelled') {
          this.booking.cancellation_date = new Date().toISOString()
        } else {
          this.booking.cancellation_date = null
        }
      } catch (e) {
        this.actionError = e.response?.data?.message || 'Failed to update booking'
      } finally {
        this.actionLoading = false
      }
    }
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

.banner {
  padding: 20px 24px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e0e0e0;
  background: white;
}

.banner-label {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.banner-date {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-top: 2px;
}

.cancel-notice {
  background: #fff3cd;
  border: 1px solid #f0ad4e;
  color: #856404;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
}

.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 650px) {
  .two-col {
    grid-template-columns: 1fr;
  }
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

.info-item {
  margin-bottom: 14px;
}

.info-item label {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7f8c8d;
  display: block;
  margin-bottom: 3px;
}

.info-item p {
  font-size: 0.95rem;
  color: #2c3e50;
}

.link {
  color: #2980b9;
  cursor: pointer;
  text-decoration: underline;
}

.link:hover {
  color: #1a6fa0;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
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
  background: #cce5ff;
  color: #004085;
}

.badge-pending {
  background: #fff3cd;
  color: #856404;
}

.badge-closed {
  background: #f8d7da;
  color: #721c24;
}

.badge-approved {
  background: #d4edda;
  color: #155724;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.error-msg {
  color: #e74c3c;
  background: #fdf0f0;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
}

.actions-card {
  margin-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
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

.btn-success {
  background: #2ecc71;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.btn-success:hover {
  background: #27ae60;
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

.success-msg {
  color: #155724;
  background: #d4edda;
  padding: 8px 14px;
  border-radius: 6px;
  margin-top: 12px;
  font-size: 0.9rem;
}

.loading-inline {
  color: #7f8c8d;
  font-size: 0.9rem;
}
</style>
