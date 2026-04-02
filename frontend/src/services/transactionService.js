import { django } from '../api';

export const fetchTransactions = (params = {}) => django.get('/transactions/', { params });
export const exportTransactions = () => django.get('/admin/export-transactions/', { responseType: 'blob' });
export const dailySummary = () => django.get('/admin/daily-summary/');
