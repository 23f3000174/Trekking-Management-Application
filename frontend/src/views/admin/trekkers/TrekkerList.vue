<template>
  <div class="page">

    <div class="page-header">
      <div>
        <h1>Trekkers</h1>
        <p class="subtitle">All registered trekkers in the system</p>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading trekkers...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else>
      <div v-if="trekkers.length === 0" class="empty-state">
        <p>No trekkers registered yet.</p>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Email</th>
            <th>Mobile</th>
            <th>Gender</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in trekkers" :key="t.id" class="clickable-row" @click="$router.push(`/admin/trekkers/${t.id}`)">
            <td>{{ t.id }}</td>
            <td>{{ t.full_name }}</td>
            <td>{{ t.email }}</td>
            <td>{{ t.mobile_no }}</td>
            <td class="capitalize">{{ t.gender }}</td>
            <td>
              <span class="badge" :class="{
                'badge-active': t.flag === 'active',
                'badge-inactive': t.flag === 'inactive',
                'badge-blacklisted': t.flag === 'blacklisted'
              }">
                {{ t.flag }}
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
  name: 'TrekkerList',

  data() {
    return {
      trekkers: [],
      loading: true,
      error: '',
    }
  },

  async mounted() {
    try {
      const res = await api.get('/admin/trekker_list')
      this.trekkers = res.data
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load trekkers'
    } finally {
      this.loading = false
    }
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
  font-size: 0.95rem;
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
