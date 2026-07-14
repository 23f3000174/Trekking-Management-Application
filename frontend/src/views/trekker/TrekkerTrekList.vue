<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1>Browse Treks</h1>
        <p class="subtitle">Open treks available for booking</p>
      </div>
      <button class="btn-secondary" @click="$router.push('/trekker/dashboard')">
        ← Dashboard
      </button>
    </div>

    <div class="card filter-card">
      <h3>Filter</h3>
      <div class="filter-grid">
        <div class="form-group">
          <label>Difficulty</label>
          <select v-model="filters.difficulty">
            <option value="">Any</option>
            <option value="easy">Easy</option>
            <option value="moderate">Moderate</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <div class="form-group">
          <label>Location</label>
          <input v-model="filters.location" type="text" placeholder="e.g. Manali" />
        </div>
        <div class="form-group">
          <label>Duration (days)</label>
          <input v-model="filters.duration" type="number" min="1" placeholder="Any" />
        </div>
      </div>
      <div class="filter-actions">
        <button class="btn-primary" @click="applyFilters">Apply Filters</button>
        <button class="btn-secondary" @click="clearFilters">Clear</button>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading treks...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else>
      <div v-if="treks.length === 0" class="empty-state">
        <p>No treks match your filters.</p>
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
            <th>End Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in treks" :key="t.id" class="clickable-row"
              @click="$router.push(`/trekker/treks/${t.id}`)">
            <td>{{ t.id }}</td>
            <td>{{ t.trek_name }}</td>
            <td>{{ t.trek_location }}</td>
            <td class="capitalize">{{ t.difficulty }}</td>
            <td>{{ t.duration_days }} days</td>
            <td>{{ t.available_slot }} / {{ t.total_slot }}</td>
            <td>{{ formatDate(t.start_date) }}</td>
            <td>{{ formatDate(t.end_date) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../../api'

export default {
  name: 'TrekkerTrekList',

  data() {
    return {
      treks: [],
      loading: true,
      error: '',
      filters: {
        difficulty: '',
        location: '',
        duration: '',
      },
    }
  },

  async mounted() {
    await this.fetchTreks()
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

    async fetchTreks() {
      this.loading = true
      this.error = ''
      const params = {}
      if (this.filters.difficulty) params.difficulty = this.filters.difficulty
      if (this.filters.location) params.location = this.filters.location
      if (this.filters.duration) params.duration = this.filters.duration

      try {
        const res = await api.get('/trekker/treks', { params })
        this.treks = res.data
      } catch (e) {
        this.error = e.response?.data?.message || 'Failed to load treks'
      } finally {
        this.loading = false
      }
    },

    async applyFilters() {
      await this.fetchTreks()
    },

    async clearFilters() {
      this.filters = { difficulty: '', location: '', duration: '' }
      await this.fetchTreks()
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

.card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 24px;
  margin-bottom: 20px;
}

.card h3 {
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 14px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.form-group {
  margin-bottom: 4px;
}

.form-group label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 6px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.92rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #2c3e50;
}

.filter-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-state p {
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
