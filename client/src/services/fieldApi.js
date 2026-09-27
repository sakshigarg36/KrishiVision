import { request } from './api.js';
export const listFields = () => request('/fields');
export const getField = (id) => request(`/fields/${encodeURIComponent(id)}`);
