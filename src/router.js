import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'login' },
  { path: '/dashboard', name: 'dashboard', meta: { auth: true } },
  { path: '/search/new', name: 'new-search', meta: { auth: true } },
  { path: '/search/:id/processing', name: 'processing', meta: { auth: true } },
  { path: '/search/:id/results', name: 'results', meta: { auth: true } },
  { path: '/search-result/:resultId', name: 'detail', meta: { auth: true } },
  { path: '/trends', name: 'trends', meta: { auth: true } },
  { path: '/my', name: 'my', meta: { auth: true } },
  { path: '/admin', name: 'admin', meta: { auth: true, admin: true } },
  { path: '/', redirect: '/dashboard' },
]
const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach((to) => {
  const loggedIn = Boolean(localStorage.getItem('patentmind_token'))
  const user = JSON.parse(localStorage.getItem('patentmind_user') || 'null')
  if (to.meta.auth && !loggedIn) return '/login'
  if (to.meta.admin && user?.role !== 'admin') return '/dashboard'
  if (to.name === 'login' && loggedIn) return '/dashboard'
})
export default router
