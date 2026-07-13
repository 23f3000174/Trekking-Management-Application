import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'

import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminSearch from '../views/admin/AdminSearch.vue'

import StaffList from '../views/admin/staff/StaffList.vue'
import StaffDetail from '../views/admin/staff/StaffDetail.vue'
import StaffCreate from '../views/admin/staff/StaffCreate.vue'

import TrekkerList from '../views/admin/trekkers/TrekkerList.vue'
import TrekkerDetail from '../views/admin/trekkers/TrekkerDetail.vue'

import TrekList from '../views/admin/treks/TrekList.vue'
import TrekDetail from '../views/admin/treks/TrekDetail.vue'
import TrekCreate from '../views/admin/treks/TrekCreate.vue'

import BookingList from '../views/admin/bookings/BookingList.vue'
import BookingDetail from '../views/admin/bookings/BookingDetail.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/login', name: 'Login', component: LoginView },

  { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/admin/search', name: 'AdminSearch', component: AdminSearch },

  { path: '/admin/staff/create', name: 'StaffCreate', component: StaffCreate },
  { path: '/admin/staff', name: 'StaffList', component: StaffList },
  { path: '/admin/staff/:id', name: 'StaffDetail', component: StaffDetail },

  { path: '/admin/trekkers', name: 'TrekkerList', component: TrekkerList },
  { path: '/admin/trekkers/:id', name: 'TrekkerDetail', component: TrekkerDetail },

  { path: '/admin/treks/create', name: 'TrekCreate', component: TrekCreate },
  { path: '/admin/treks', name: 'TrekList', component: TrekList },
  { path: '/admin/treks/:id', name: 'TrekDetail', component: TrekDetail },

  { path: '/admin/bookings', name: 'BookingList', component: BookingList },
  { path: '/admin/bookings/:id', name: 'BookingDetail', component: BookingDetail },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
