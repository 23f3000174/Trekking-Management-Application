import { createRouter, createWebHistory } from 'vue-router'

import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'

import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  {path : '/register', component : RegisterView},
  {path : '/login', component : LoginView},

  {path : '/admin/dashboard', component : AdminDashboard},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
