import axios from 'axios';

export const django = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: { 'Content-Type': 'application/json' },
});

export const fastapi = axios.create({
  baseURL: 'http://127.0.0.1:8100',
  headers: { 'Content-Type': 'application/json' },
});

export const setAuthToken = (token) => {
  if (token) {
    django.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete django.defaults.headers.common.Authorization;
  }
};
