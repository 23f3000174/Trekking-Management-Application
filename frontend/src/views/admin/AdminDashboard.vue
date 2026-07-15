<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>Admin dashboard</h1>
      <p class="subtitle">Overview of the entire trekking system</p>
    </div>

    <div v-if="loading" class="loading">Loading Dashboard...</div>

    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="stats-grid">
      <div v-for="card in statCards" :key="card.label" class="stat-card" @click="$router.push(card.route)">
        <span class="card-icon">{{ card.icon }}</span>
        <div class="card-body">
          <p class="card-label">{{ card.label }}</p>
          <p class="card-value">{{ card.value }}</p>
        </div>
        <span class="card-arrow"> -> </span>
      </div>
    </div>

    <div v-if="!loading && !error" class="quick-action">
      <h2>Quick Action</h2>
      <div class="action-buttons">
        <button @click="$router.push('/admin/staff/create')" class="btn-primary">
          + Add Staff
        </button>
        <button @click="$router.push('/admin/treks/create')" class="btn-primary">
          + Add Trek
        </button>
        <button @click="$router.push('/admin/search')" class="btn-secondary">
          + Search
        </button>
      </div>
    </div>

  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'AdminDashboard',

  data() {
    return {
      stats: {},
      loading: true,
      error: '',
    }
  },

  computed: {
    statCards() {
      return [
        {
          label: 'Total Staff',
          value: this.stats.total_staff ?? '--',
          icon: '',
          route: '/admin/staff',
        },
        {
          label: 'Total Treks',
          value: this.stats.total_treks ?? '—',
          icon: '🏔️',
          route: '/admin/treks',
        },
        {
          label: 'Active Treks',
          value: this.stats.active_treks ?? '—',
          icon: '✅',
          route: '/admin/treks',
        },
        {
          label: 'Trekkers',
          value: this.stats.total_trekkers ?? '—',
          icon: '🧗',
          route: '/admin/trekkers',
        },
        {
          label: 'Bookings',
          value: this.stats.total_bookings ?? '—',
          icon: '📋',
          route: '/admin/bookings',
        },
      ]
    }
  },

  async mounted() {
    try {
      const res = await api.get('/admin/dashboard')
      this.stats = res.data
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load dashboard'
    } finally {
      this.loading = false
    }
  },
}
</script>

<style scoped>
.dashboard {
  padding: 20px 0;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 1.8rem;
  color: #2c3e50;
}

.subtitle {
  color: #7f8c8d;
  margin-top: 4px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.card-icon {
  font-size: 2rem;
}

.card-body {
  flex: 1;
}

.card-label {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-bottom: 4px;
}

.card-value {
  font-size: 1.6rem;
  font-weight: bold;
  color: #2c3e50;
}

.card-arrow {
  color: #bdc3c7;
  font-size: 1.2rem;
}

.quick-actions {
  border-top: 1px solid #eee;
  padding-top: 24px;
}

.quick-actions h2 {
  font-size: 1.1rem;
  margin-bottom: 14px;
  color: #2c3e50;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
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
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #f0f0f0;
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
