<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo">
        <h1>Finvee</h1>
        <p class="tagline">AI-Powered Finance & Learning</p>
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="Enter your email" required />
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Enter your password" required />
        </div>
        
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
        
        <div class="demo-hint">
          <p>Demo: demo@finvee.com / demo123</p>
        </div>
        
        <p v-if="error" class="error">{{ error }}</p>
      </form>
      
      <p class="switch-auth">
        Don't have an account? <router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const email = ref('demo@finvee.com')
const password = ref('demo123')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    console.log('Attempting login...')
    const response = await api.post('/api/auth/login', {
      email: email.value,
      password: password.value
    })
    
    console.log('Login response:', response)
    
    if (response.success === true && response.data) {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      console.log('Login successful, redirecting...')
      
      // Force page reload to ensure clean state
      window.location.href = '/dashboard'
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = err.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  width: 100%;
  max-width: 420px;
}

.logo {
  text-align: center;
  margin-bottom: 2rem;
}

.logo h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1a1a2e;
  margin: 0;
  letter-spacing: -1px;
}

.logo .tagline {
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #0f3460;
  box-shadow: 0 0 0 3px rgba(15, 52, 96, 0.1);
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(15, 52, 96, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.demo-hint {
  background: #f0f7ff;
  border-radius: 8px;
  padding: 0.75rem;
  margin-top: 1rem;
  text-align: center;
}

.demo-hint p {
  margin: 0;
  color: #0f3460;
  font-size: 0.85rem;
  font-weight: 500;
}

.error {
  color: #e74c3c;
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.switch-auth {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.switch-auth a {
  color: #0f3460;
  font-weight: 600;
  text-decoration: none;
}

.switch-auth a:hover {
  text-decoration: underline;
}
</style>