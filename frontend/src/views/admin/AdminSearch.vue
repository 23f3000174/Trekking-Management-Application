<template>
  <div class="page">
    <div class="page-header">
      <h1>Search</h1>
      <p class="subtitle">Search across staff, treks, and trekkers</p>
    </div>

    <div class="search-bar">
      <input v-model="query" type="text" placeholder="Type a name, email, or location..." class="search-input"
        @input="onInput" />

      <select v-model="searchType" class="type-select">
        <option value="all">All</option>
        <option value="trek">Treks</option>
        <option value="staff">Staff</option>
        <option value="trekker">Trekkers</option>
      </select>
    </div>

    <div v-if="loading" class="loading">Searching ...</div>

    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else-if="hasResults" class="results">
      <div v-if="results.treks && results.treks.length > 0" class="result-section">
        <h3 class="section-title">🏔️ Treks ({{ results.treks.length }})</h3>
        <div v-for="trek in results.treks" :key="'trek-' + trek.id" class="result-card"
          @click="$router.push(`/admin/treks/${trek.id}`)">
          <div class="result-main">
            <p class="result-name">{{ trek.trek_name }}</p>
            <p class="result-sub">{{ trek.trek_location }}</p>
          </div>
          <div class="result-badges">
            <span class="badge" :class="'badge-' + trek.trek_status">
              {{ trek.trek_status }}
            </span>
            <span class="badge badge-difficulty">{{ trek.difficulty }}</span>
          </div>
        </div>
      </div>

      <div v-if="results.staff && results.staff.length > 0" class="result-section">
        <h3 class="section-title">👷 Staff ({{ results.staff.length }})</h3>
        <div v-for="s in results.staff" :key="'staff-' + s.id" class="result-card"
          @click="$router.push(`/admin/staff/${s.id}`)">
          <div class="result-main">
            <p class="result-name">{{ s.full_name }}</p>
            <p class="result-sub">{{ s.email }}</p>
          </div>
          <span class="badge" :class="'badge-' + s.flag">{{ s.flag }}</span>
        </div>
      </div>

      <div v-if="results.trekkers && results.trekkers.length > 0" class="result-section">
        <h3 class="section-title">🧗 Trekkers ({{ results.trekkers.length }})</h3>
        <div v-for="t in results.trekkers" :key="'trekker-' + t.id" class="result-card"
          @click="$router.push(`/admin/trekkers/${t.id}`)">
          <div class="result-main">
            <p class="result-name">{{ t.full_name }}</p>
            <p class="result-sub">{{ t.email }}</p>
          </div>
          <span class="badge" :class="'badge-' + t.flag">{{ t.flag }}</span>
        </div>
      </div>

    </div>
    <div v-else-if="searched && !loading" class="no-results">
      <p>No results found for "<strong>{{ query }}</strong>"</p>
    </div>
  </div>
</template>

<script>
import api from '../../api'
export default {
  name: 'AdminSearch',

  data() {
    return {
      query: '',
      searchType: 'all',
      results: {},
      loading: false,
      error: '',
      searched: false,
      debounceTimer: null
    }
  },

  computed: {
    hasResults() {
      return Object.values(this.results).some(arr => Array.isArray(arr) && arr.length > 0)
    },
  },

  methods: {
    onInput() {
      clearTimeout(this.debounceTimer)

      if (!this.query.trim()) {
        this.results = {}
        this.searched = false
        return
      }

      this.debounceTimer = setTimeout(() => {
        this.search()
      }, 400)
    },

    async search() {
      this.loading = true
      this.error = ''
      try {
        const res = await api.get('/admin/search', {
          params: {
            q: this.query,
            type: this.searchType,
          }
        })
        this.results = res.data
        this.searched = true
      } catch (e) {
        this.error = e.response?.data?.message || 'Search failed'
      } finally {
        this.loading = false
      }
    },
  },

  watch: {
    searchType() {
      if (this.query.trim()) {
        this.search()
      }
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

.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #2c3e50;
  box-shadow: 0 0 0 2px rgba(44, 62, 80, 0.1);
}

.type-select {
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
  cursor: pointer;
}

.results {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.result-section {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.section-title {
  padding: 14px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  font-size: 0.95rem;
  color: #2c3e50;
  font-weight: 600;
}

.result-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: background 0.15s;
}

.result-card:last-child {
  border-bottom: none;
}

.result-card:hover {
  background: #f8f9fa;
}

.result-main {
  flex: 1;
}

.result-name {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 2px;
}

.result-sub {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.result-badges {
  display: flex;
  gap: 6px;
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

.badge-completed {
  background: #d4edda;
  color: #155724;
}

.badge-approved {
  background: #cce5ff;
  color: #004085;
}

.badge-difficulty {
  background: #e8e8e8;
  color: #444;
}

.no-results {
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
