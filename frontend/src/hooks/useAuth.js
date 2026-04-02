import { useState } from 'react';
import { django, setAuthToken } from '../api';

export function useAuth() {
  const [token, setToken] = useState(localStorage.getItem('access') || null);
  const [user, setUser] = useState(null);

  const register = async ({ username, email, password }) => {
    const res = await django.post('/auth/register/', { username, email, password });
    return res;
  };

  const login = async ({ email, password }) => {
    const res = await django.post('/auth/login/', { email, password });
    const { access, refresh } = res.data;
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
    setAuthToken(access);
    setToken(access);
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    setAuthToken(null);
    setToken(null);
    setUser(null);
  };

  if (token) {
    setAuthToken(token);
  }

  return { token, user, register, login, logout };
}
