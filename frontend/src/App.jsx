import { useState } from 'react';
import { useAuth } from './hooks/useAuth';
import CardManager from './components/CardManager';
import Payment from './components/Payment';
import { Routes, Route, Link, useNavigate, Navigate } from 'react-router-dom';

function LoginForm({ onLogin, form, setForm, error }) {
  return (
    <div>
      <input
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
        placeholder="Email"
      />
      <input
        type="password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
        placeholder="Password"
      />
      <button onClick={onLogin}>Login</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <div>
        <Link to="/register">Don't have an account? Register</Link>
      </div>
    </div>
  );
}

function RegisterForm({ onRegister, form, setForm, error }) {
  return (
    <div>
      <input
        value={form.username}
        onChange={(e) => setForm({ ...form, username: e.target.value })}
        placeholder="Username"
      />
      <input
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
        placeholder="Email"
      />
      <input
        type="password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
        placeholder="Password"
      />
      <button onClick={onRegister}>Register</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <div>
        <Link to="/login">Already have an account? Login</Link>
      </div>
    </div>
  );
}

function AuthRoutes({ onLogin, onRegister, form, setForm, error }) {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm onLogin={onLogin} form={form} setForm={setForm} error={error} />} />
      <Route path="/register" element={<RegisterForm onRegister={onRegister} form={form} setForm={setForm} error={error} />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function App() {
  const { token, login, register, logout } = useAuth();
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    setError('');
    try {
      await register(form);
      alert('Registration successful, login now.');
      navigate('/login');
    } catch (err) {
      setError('Registration failed. Please check your details.');
    }
  };

  const handleLogin = async () => {
    setError('');
    try {
      await login({ email: form.email, password: form.password });
      alert('Login successful');
      navigate('/cards');
    } catch (err) {
      setError('Incorrect email or password.');
    }
  };

  if (!token) {
    return (
      <AuthRoutes
        onLogin={handleLogin}
        onRegister={handleRegister}
        form={form}
        setForm={setForm}
        error={error}
      />
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4">
      <header className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Credit Card Dashboard</h1>
        <nav>
          <Link to="/cards" className="mr-4">Cards</Link>
          <Link to="/payments" className="mr-4">Payments</Link>
          <button onClick={logout} className="bg-red-600 text-white px-4 py-2 rounded">Logout</button>
        </nav>
      </header>
      <Routes>
        <Route path="/cards" element={<CardManager />} />
        <Route path="/payments" element={<Payment />} />
        <Route path="*" element={<Navigate to="/cards" />} />
      </Routes>
    </div>
  );
}

export default App;
