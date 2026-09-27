import { request } from './api.js';
export const login = (credentials) => request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) });
export const register = (details) => request('/auth/register', { method: 'POST', body: JSON.stringify(details) });
