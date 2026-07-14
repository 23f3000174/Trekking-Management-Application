<template>
  <div class="page">

    <button class="btn-primary" @click="$router.push('admin/staff')">
      ← Back to Staff List
    </button>

    <div v-if="loading" class="loading">Loading staff details...</div>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div v-else class="content">
      <div class="card profile-card">
        <div class="card-header">
          <div class="avatar">{{ initials }}</div>
          <div>
            <h2>{{ staff.full_name }}</h2>
            <p class="email">{{ staff.email }}</p>

            <span class="badge" :class="{
              'badge-active': staff.flag === 'active',
              'badge-inactive': staff.flag === 'inactive',
              'badge-blacklisted': staff.flag === 'blacklisted'
            }">
              {{ staff.flag }}
            </span>
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <label>Mobile</label>
            <p>{{ staff.mobile_no || '--' }}</p>
          </div>
          <div class="info-item">
            <label>Contact</label>
            <p>{{ staff.contact || '--' }}</p>
          </div>
          <div class="info-item">
            <label>Bio</label>
            <p>{{ staff.bio || '--' }}</p>
          </div>
          <div class="info-item">
            <label>Staff Status</label>
            <p>{{ staff.status || '--' }}</p>
          </div>
        </div>

        <div class="card-action">
          <button class="btn-secondary" @click="showEditForm = !showEditForm">
            {{ showEditForm ? 'Cancle Edit' : '✏️ Edit' }}
          </button>
          <button class="btn-warning" @click="toggleBlacklist" :disabled="actionLoading">
            {{ staff.flag === 'blacklisted' ? '✅ Reactivate' : '🚫 Blacklist' }}
          </button>

          <button class="btn-danger" @click="deleteStaff" :disabled="actionLoading">
            🗑️ Delete
          </button>
        </div>
      </div>

      <div v-show="showEditForm" class="card edit-card">
        <h3>Edit Staff Details</h3>
        <div class="form-group">
          <label>Full Name</label>
          <input v-model="editForm.full_name" type="text" />
        </div>
        <div class="form-group">
          <label>Mobile</label>
          <input v-model="editForm.mobile_no" type="text" />
        </div>
        <div class="form-group">
          <label>Account Flag</label>
          <select v-model="editForm.flag">
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="blacklisted">Blacklisted</option>
          </select>
        </div>
        <p v-if="updateMsg" class="success-msg">{{ updateMsg }}</p>
        <button class="btn-primary" @click="updateStaff" :disabled="actionLoading">
          Save Changes
        </button>
      </div>


      <div class="card">
        <h3>Assigned Treks</h3>
        <div v-if="staff.assigned_treks && staff.assigned_treks.length === 0" class="empty">
          No treks assigned yet.
        </div>
        <table v-else class="data-table">
          <thead>
            <tr>
              <th>Trek Name</th>
              <th>Status</th>
              <th>Start Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in staff.assigned_treks" :key="trek.trek_id" class="clickable-row"
              @click="$router.push(`/admin/treks/${trek.trek_id}`)">
              <td>{{ trek.trek_name }}</td>
              <td>
                <span class="badge" :class="'badge-' + trek.trek_status">
                  {{ trek.trek_status }}
                </span>
              </td>
              <td>{{ trek.start_date }}</td>
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
  name: 'StaffDetail',

  data() {
    return {
      staff: {},
      loading: true,
      error: '',
      showEditForm: false,
      actionLoading: false,
      updateMsg: '',
      editForm: {
        full_name: '',
        mobile_no: '',
        flag: '',
      },
    }
  },

  computed: {
    initials() {
      if (!this.staff.full_name) return '?'

      return this.staff.full_name
        .split(' ')
        .map(w => w[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    },
  },

  async mounted() {
    const id = this.$route.params.id
    try {
      const res = await api.get(`/admin/staff/${id}`)
      this.staff = res.data
      this.editForm = {
        full_name: this.staff.full_name,
        mobile_no: this.staff.mobile_no,
        contact: this.staff.contact,
        bio: this.staff.bio,
        flag: this.staff.flag,
      }
    } catch (e) {
      this.error = e.response?.data?.message || 'Failed to load staff'
    } finally {
      this.loading = false
    }
  },

  methods: {
    async updateStaff() {
      this.actionLoading = true
      try {
        await api.put(`admin/staff/${this.staff.id}`, this.editForm)
        this.staff.full_name = this.editForm.full_name
        this.staff.flag = this.editForm.flag
        this.updateMsg = 'Staff updated successfully!'

        setTimeout(() => {
          this.updateMsg = ''
          this.showEditForm = false
        }, 1500)
      } catch (e) {
        this.error = e.response?.data?.message || 'Update failed'
      } finally {
        this.actionLoading = false
      }
    },

    async toggleBlacklist() {
      this.actionLoading = true
      const newFlag = this.staff.flag === 'blacklisted' ? 'active' : 'blacklisted'
      try {
        await api.put(`/admin/staff/${this.staff.id}`, { flag: newFlag })
        this.staff.flag = newFlag
      } catch (e) {
        this.error = e.response?.data?.message || 'Action failed'
      } finally {
        this.actionLoading = false
      }
    },

    async deleteStaff() {
      if (!confirm(`Delete ${this.staff.full_name}? This cannot be undone.`))
        return this.actionLoading = true
      try {
        await api.delete(`/admin/staff/${this.staff.id}`)
        this.$router.push('/admin/staff')
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

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  background: #2c3e50;
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
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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

.card-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.edit-card {
  border-left: 4px solid #3498db;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  color: #555;
  margin-bottom: 6px;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #2c3e50;
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

.btn-warning {
  background: #f39c12;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-danger {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
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
  margin-bottom: 12px;
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
