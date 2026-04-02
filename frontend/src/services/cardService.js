import { django } from '../api';

export const fetchCards = () => django.get('/cards/');
export const addCard = (payload) => django.post('/cards/', payload);
export const deleteCard = (id) => django.delete(`/cards/${id}/`);
