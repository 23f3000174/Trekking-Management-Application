<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1>Trekker Dashboard</h1>
        <p class="subtitle">Welcome, {{ profile.full_name }}</p>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading dashboard...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="content">
      <div class="stat-cards">
        <div class="stat-card">
          <span class="stat-value">{{ profile.total_available || 0 }}</span>
          <span class="stat-label">Open Treks</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ profile.total_bookings || 0 }}</span>
          <span class="stat-label">My Bookings</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ activeBookings }}</span>
          <span class="stat-label">Active Bookings</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title-row">
          <h3>Available Treks</h3>
          <button class="btn-secondary" @click="$router.push('/trekker/treks')">Browse All</button>
        </div>

        <div v-if="profile.available_treks && profile.available_treks.length === 0" class="empty">
          No treks open for booking right now.
        </div>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Trek Name</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Duration</th>
              <th>Slots</th>
              <th>Start Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in profile.available_treks" :key="t.id" class="clickable-row"
                @click="$router.push(`/trekker/treks/${t.id}`)">
              <td>{{ t.id }}</td>
              <td>{{ t.trek_name }}</td>
              <td>{{ t.trek_location }}</td>
              <td class="capitalize">{{ t.difficulty }}</td>
              <td>{{ t.duration_days }} days</td>
              <td>{{ t.available_slot }} / {{ t.total_slot }}</td>
              <td>{{ formatDate(t.start_date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="card">
        <div class="card-title-row">
          <h3>My Bookings</h3>
          <button class="btn-secondary" @click="$router.push('/trekker/bookings')">View All</button>
        </div>

        <div v-if="profile.my_bookings && profile.my_bookings.length === 0" class="empty">
          You have no bookings yet.
        </div>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Trek</th>
              <th>Location</th>
              <th>Trek Status</th>
              <th>Booking Status</th>
              <th>Start Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in profile.my_bookings" :key="b.booking_id" class="clickable-row"
                @click="$router.push(`/trekker/bookings/${b.booking_id}`)">
              <td>{{ b.trek_name }}</td>
              <td>{{ b.trek_location }}</td>
              <td>
                <span class="badge" :class="'badge-' + b.trek_status">{{ b.trek_status }}</span>
              </td>
              <td>
                <span class="badge" :class="'badge-' + b.booking_status">{{ b.booking_status }}</span>
              </td>
              <td>{{ formatDate(b.start_date) }}</td>
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
  name: 'TrekkerDashboard',

  data() {
    return {
      profile: {},
      loading: true,
      error: '',
    }
  },

  computed: {
    activeBookings() {
      if (!this.profile.my_bookings) return 0
      return this.profile.my_bookings.filter(b => b.booking_status === 'booked').length
    },
  },

  async mounted() {
    try {
      const res = await api.get('/trekker/dashboard')
      this.profile = res.data
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load dashboard'
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

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.stat-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7f8c8d;
}

.card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 24px;
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
  font-size: 1.05rem;
  color: #2c3e50;
  margin: 0;
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

.clickable-row {
  cursor: pointer;
  transition: background 0.15s;
}

.clickable-row:hover {
  background: #f8f9fa;
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

.btn-secondary {
  background: white;
  color: #2c3e50;
  border: 1px solid #2c3e50;
  padding: 7px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
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

.error-msg {
  color: #e74c3c;
  background: #fdf0f0;
  padding: 10px 16px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
}
</style>
