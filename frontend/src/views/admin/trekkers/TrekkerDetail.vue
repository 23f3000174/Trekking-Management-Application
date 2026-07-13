<template>
  <div class="page">

    <button class="btn-back" @click="$router.push('/admin/trekkers')">
      ← Back to Trekkers
    </button>

    <div v-if="loading" class="loading">Loading trekker details...</div>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="content">

      <div class="card profile-card">
        <div class="card-header">
          <div class="avatar">{{ initials }}</div>
          <div>
            <h2>{{ trekker.full_name }}</h2>
            <p class="email">{{ trekker.email }}</p>
            <span class="badge" :class="{
              'badge-active': trekker.flag === 'active',
              'badge-inactive': trekker.flag === 'inactive',
              'badge-blacklisted': trekker.flag === 'blacklisted'
            }">
              {{ trekker.flag }}
            </span>
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <label>Mobile</label>
            <p>{{ trekker.mobile_no || '—' }}</p>
          </div>
          <div class="info-item">
            <label>Date of Birth</label>
            <p>{{ formattedDob }}</p>
          </div>
          <div class="info-item">
            <label>Gender</label>
            <p class="capitalize">{{ trekker.gender || '—' }}</p>
          </div>
          <div class="info-item">
            <label>Emergency Contact</label>
            <p>{{ trekker.emergency_contact || '—' }}</p>
          </div>
        </div>

        <div class="card-actions">
          <button class="btn-warning" @click="toggleBlacklist" :disabled="actionLoading">
            {{ trekker.flag === 'blacklisted' ? '✅ Reactivate' : '🚫 Blacklist' }}
          </button>

          <button class="btn-danger" @click="deleteTrekker" :disabled="actionLoading">
            🗑️ Delete Account
          </button>
        </div>

        <p v-if="actionMsg" class="success-msg" style="margin-top: 12px;">
          {{ actionMsg }}
        </p>
      </div>

      <div class="card">
        <h3>Booking History ({{ trekker.booking_history?.length || 0 }})</h3>

        <div v-if="!trekker.booking_history || trekker.booking_history.length === 0" class="empty">
          No bookings yet.
        </div>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Booking ID</th>
              <th>Trek Name</th>
              <th>Location</th>
              <th>Booked On</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in trekker.booking_history" :key="b.booking_id" class="clickable-row"
              @click="$router.push(`/admin/bookings/${b.booking_id}`)">
              <td>#{{ b.booking_id }}</td>
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
  </div>
</template>

<script>
import api from '../../../api'

export default {
  name: 'TrekkerDetail',

  data() {
    return {
      trekker: {},
      loading: true,
      error: '',
      actionLoading: false,
      actionMsg: '',
    }
  },

  computed: {
    initials() {
      if (!this.trekker.full_name) return '?'
      return this.trekker.full_name
        .split(' ')
        .map(w => w[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    },

    formattedDob() {
      if (!this.trekker.dob) return '—'
      return new Date(this.trekker.dob).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    },
  },

  async mounted() {
    const id = this.$route.params.id
    try {
      const res = await api.get(`/admin/trekker/${id}`)
      this.trekker = res.data
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load trekker'
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

    async toggleBlacklist() {
      this.actionLoading = true
      const newFlag = this.trekker.flag === 'blacklisted' ? 'active' : 'blacklisted'
      try {
        await api.put(`/admin/trekker/${this.trekker.id}`, { flag: newFlag })
        this.trekker.flag = newFlag
        this.actionMsg = `Account ${newFlag === 'blacklisted' ? 'blacklisted' : 'reactivated'}.`
        setTimeout(() => { this.actionMsg = '' }, 2000)
      } catch (e) {
        this.error = e.response?.data?.message || 'Action failed'
      } finally {
        this.actionLoading = false
      }
    },

    async deleteTrekker() {
      if (!confirm(`Delete ${this.trekker.full_name}? This cannot be undone.`)) return
      this.actionLoading = true
      try {
        await api.delete(`/admin/trekker/${this.trekker.id}`)
        this.$router.push('/admin/trekkers')
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

.card-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #27ae60;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  font-weight: bold;
  flex-shrink: 0;
}

.email {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 4px 0 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
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
  flex-wrap: wrap;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
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

.badge-active {
  background: #d4edda;
  color: #155724;
}

.badge-inactive {
  background: #fff3cd;
  color: #856404;
}

.badge-blacklisted {
  background: #f8d7da;
  color: #721c24;
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

.btn-warning {
  background: #f39c12;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.btn-danger {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.2s;
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

.empty {
  color: #7f8c8d;
  font-size: 0.9rem;
  padding: 10px 0;
}
</style>
