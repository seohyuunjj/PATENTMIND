import axios from 'axios'
import { mockResults, mockSearches, mockUser } from './mocks'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080', timeout: 7000 })
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('patentmind_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export async function request(config, fallback) {
  if (import.meta.env.VITE_API_MOCK !== 'false') return Promise.resolve(fallback)
  try { return (await api(config)).data } catch (error) {
    if (error.response?.status === 401) { localStorage.removeItem('patentmind_token'); window.location.href = '/login' }
    return fallback
  }
}

export const authApi = { login: (payload) => request({ method: 'post', url: '/api/auth/login', data: payload }, { token: 'mock-token', user: { ...mockUser, name: payload.name || mockUser.name } }) }
export const searchApi = {
  list: () => request({ method: 'get', url: '/api/searches' }, mockSearches),
  create: (payload) => request({ method: 'post', url: '/api/searches', data: payload }, { id: `PM-${Date.now().toString().slice(-4)}`, ...payload }),
  status: (id) => request({ method: 'get', url: `/api/searches/${id}/status` }, { id, progress: 100, step: 4, status: 'completed' }),
  results: (id, tier) => request({ method: 'get', url: `/api/searches/${id}/results`, params: { tier } }, tier && tier !== 'All' ? mockResults.filter((item) => item.tier === tier) : mockResults),
  expand: (query) => request({ method: 'post', url: '/api/searches/expand', data: { query } }, { synonyms: ['고체 전해질', 'solid-state electrolyte', '황화물계 전해질', 'sulfide-based electrolyte'], ipcCodes: ['H01M 10/052', 'H01M 4/136', 'C01B 17/22'] }),
}
export const resultApi = { detail: (id) => request({ method: 'get', url: `/api/search-results/${id}` }, mockResults.find((item) => item.id === id) || mockResults[0]), confirm: (id, data) => request({ method: 'patch', url: `/api/search-results/${id}/confirm-tag`, data }, { ok: true }) }
export const trendApi = { applicants: () => request({ method: 'get', url: '/api/trends/applicant-trend' }, [{ year: 2022, value: 36 }, { year: 2023, value: 52 }, { year: 2024, value: 74 }, { year: 2025, value: 98 }, { year: 2026, value: 126 }]), heatmap: () => request({ method: 'get', url: '/api/trends/whitespace-heatmap' }, [[3, 5, 2, 4], [7, 8, 6, 3], [2, 4, 9, 6], [5, 3, 7, 8]]) }
export const adminApi = { logs: () => request({ method: 'get', url: '/api/admin/sync-logs' }, [{ source: 'KIPRIS', time: '2026.09.08 09:24', status: '완료', records: '2,481' }, { source: 'Google Patents', time: '2026.09.08 08:10', status: '완료', records: '1,832' }, { source: 'USPTO', time: '2026.09.07 22:40', status: '진행 중', records: '—' }]) }
