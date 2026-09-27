import { request } from './api.js';
export const predictYield = (payload) => request('/yield/predict', { method: 'POST', body: JSON.stringify(payload) });
export const detectDisease = (payload) => request('/disease/detect', { method: 'POST', body: JSON.stringify(payload) });
