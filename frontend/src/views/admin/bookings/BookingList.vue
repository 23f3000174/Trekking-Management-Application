<template>
  <div class="page">

    <div class="page-header">
      <div>
        <h1>All Bookings</h1>
        <p class="subtitle">Complete booking history across all treks</p>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading bookings...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else>
      <div v-if="bookings.length === 0" class="empty-state">
        <p>No bookings found.</p>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>User</th>
            <th>Trek</th>
            <th>Location</th>
            <th>Booked On</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in bookings" :key="b.booking_id" class="clickable-row"
            @click="$router.push(`/admin/bookings/${b.booking_id}`)">
            <td>#{{ b.booking_id }}</td>
            <td>{{ b.user_name }}</td>
            <td>{{ b.trek_name }}</td>
            <td>{{ b.trek_location }}</td>
            <td>{{ formatDate(b.booking_date) }}</td>
            <td>
              <span class="badge" :class="{
                'badge-booked': b.booking_status === 'booked',
                'badge-cancelled': b.booking_status === 'cancelled',
                'badge-completed': b.booking_status === 'completed'
              }">
                {{ b.booking_status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import api from '../../../api'

export default {
  name: 'BookingList',

  data() {
    return {
      bookings: [],
      loading: true,
      error: '',
    }
  },

  async mounted() {
    try {
      const res = await api.get('/admin/bookings')
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
        year: 'numeric', month: 'short', day: 'numeric'
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
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
