<template>
  <div class="page">

    <div class="page-header">
      <div>
        <h1>Staff Members</h1>
        <p class="subtitle">All trek staff in the system</p>
      </div>
      <button class="btn-primary" @click="$router.push('/admin/staff/create')">
        + Add Staff
      </button>
    </div>

    <div v-if="loading" class="loading">Loading staff...</div>
    <p v-else-if="error" class="error-msg">{{ error }}</p>

    <div v-else>
      <div v-if="staff.length === 0" class="empty-state">
        <p>No staff members found.</p>
        <button class="btn-primary" @click="$router.push('/admin/staff/create')">
          Add the first staff member
        </button>
      </div>

    <table v-else class="data-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
          <th>Mobile</th>
          <th>Account Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in staff" :key="s.id" class="clickable-row"
            @click="$router.push(`/admin/staff/${s.id}`)">
          <td>{{ s.id }}</td>
          <td>{{ s.full_name }}</td>
          <td>{{ s.email}}</td>
          <td>{{ s.mobile_no }}</td>
          <td>
            <span class="badge" :class="{
              'badge-active' : s.flag === 'active',
              'badge-inactive' : s.flag === 'inactive',
              'badge-blacklisted' : s.flag === 'blacklisted',
              }">
              {{ s.flag }}
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
  name: 'StaffList',

  data() {
    return {
      staff : [],
      loading : true,
      error : '',
    }
  },

  async mounted() {
    try {
      const res = await api.get('/admin/staff_list')
      this.staff = res.data
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load staff'
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
  font-weight: 600;
  font-size: 0.85rem;
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

/* Status badges */
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
