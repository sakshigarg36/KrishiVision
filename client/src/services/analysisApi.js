import { request } from './api.js';
export const listAnalyses = () => request('/analysis');
export const createAnalysis = (payload) => request('/analysis', { method: 'POST', body: JSON.stringify(payload) });
