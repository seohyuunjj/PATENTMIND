import { defineStore } from 'pinia'
import { authApi } from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: JSON.parse(localStorage.getItem('patentmind_user') || 'null'), token: localStorage.getItem('patentmind_token') }),
  getters: { isAuthenticated: (state) => Boolean(state.token) },
  actions: {
    async login(payload) { const data = await authApi.login(payload); this.token = data.token; this.user = data.user; localStorage.setItem('patentmind_token', data.token); localStorage.setItem('patentmind_user', JSON.stringify(data.user)) },
    logout() { this.token = null; this.user = null; localStorage.removeItem('patentmind_token'); localStorage.removeItem('patentmind_user') },
  },
})
