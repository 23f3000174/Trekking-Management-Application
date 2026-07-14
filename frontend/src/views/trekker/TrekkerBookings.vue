<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1>My Bookings</h1>
        <p class="subtitle">Your trekking history</p>
      </div>
      <button class="btn-secondary" @click="$router.push('/trekker/treks')">
        Browse Treks
      </button>
    </div>

    <div v-if="loading" class="loading">Loading bookings...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else>
      <div v-if="bookings.length === 0" class="empty-state">
        <p>You have no bookings yet.</p>
        <button class="btn-primary" @click="$router.push('/trekker/treks')">
          Browse available treks
        </button>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Trek Name</th>
            <th>Location</th>
            <th>Difficulty</th>
            <th>Trek Status</th>
            <th>Booking Status</th>
            <th>Booked On</th>
            <th>Start Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in bookings" :key="b.booking_id" class="clickable-row"
              @click="$router.push(`/trekker/bookings/${b.booking_id}`)">
            <td>{{ b.booking_id }}</td>
            <td>{{ b.trek_name }}</td>
            <td>{{ b.trek_location }}</td>
            <td class="capitalize">{{ b.difficulty }}</td>
            <td>
              <span class="badge" :class="'badge-' + b.trek_status">{{ b.trek_status }}</span>
            </td>
            <td>
              <span class="badge" :class="'badge-' + b.booking_status">{{ b.booking_status }}</span>
            </td>
            <td>{{ formatDate(b.booking_date) }}</td>
            <td>{{ formatDate(b.start_date) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'TrekkerBookings',

  data() {
    return {
      bookings: [],
      loading: true,
      error: '',
    }
  },

  async mounted() {
    try {
      const res = await api.get('/trekker/bookings')
      this.bookings = res.data
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load bookings'
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
  },
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
}

.subtitle {
  color: #7f8c8d;
  margin-top: 4px;
  font-size: 0.9rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.data-table thead {
  background: #2c3e50;
  color: white;
}

.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.92rem;
}

.clickable-row {
  cursor: pointer;
  transition: background 0.15s;
}

.clickable-row:hover {
  background: #f8f9fa;
}

.clickable-row:last-child td {
  border-bottom: none;
}

.capitalize {
  text-transform: capitalize;
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: capitalize;
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

.btn-secondary {
  background: white;
  color: #2c3e50;
  border: 1px solid #2c3e50;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-state p {
  margin-bottom: 16px;
  font-size: 1.1rem;
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
</style>
