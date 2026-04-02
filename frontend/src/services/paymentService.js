import { fastapi } from '../api';

export const makePayment = (payload) => fastapi.post('/payments', payload);
export const paymentHealth = () => fastapi.get('/health');
