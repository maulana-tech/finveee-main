<template>
  <div class="login-page">
    <!-- Left Side - Branding -->
    <div class="login-branding">
      <div class="brand-content">
        <div class="brand-logo">■</div>
        <div class="brand-name">FINVEE</div>
        <div class="brand-desc">AI-Powered Finance, Learning & Swarm Intelligence</div>
        
        <div class="brand-features">
          <div class="feature">
            <span class="feature-icon">[$]</span>
            <span>Financial Management</span>
          </div>
          <div class="feature">
            <span class="feature-icon">[#]</span>
            <span>AI Learning</span>
          </div>
          <div class="feature">
            <span class="feature-icon">[S]</span>
            <span>Swarm Simulation</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side - Login Form -->
    <div class="login-form-section">
      <div class="login-card">
        <div class="card-header">
          <h1>SIGN_IN</h1>
          <p class="card-subtitle">Welcome back to Finvee</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label>EMAIL</label>
            <input 
              v-model="email" 
              type="email" 
              placeholder="Enter your email" 
              required 
            />
          </div>
          
          <div class="form-group">
            <label>PASSWORD</label>
            <input 
              v-model="password" 
              type="password" 
              placeholder="Enter your password" 
              required 
            />
          </div>
          
          <button type="submit" class="btn-login" :disabled="loading">
            {{ loading ? 'LOGGING_IN...' : 'LOGIN' }}
          </button>
          
          <div v-if="error" class="error-box">
            {{ error }}
          </div>
        </form>

        <div class="demo-box">
          <div class="demo-label">DEMO_ACCOUNT</div>
          <div class="demo-creds">demo@finvee.com / demo123</div>
        </div>

        <div class="auth-switch">
          Don't have an account? 
          <router-link to="/register">Register</router-link>
        </div>
      </div>
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
    const response = await api.post('/api/auth/login', {
      email: email.value,
      password: password.value
    })
    
    if (response.success === true && response.data) {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

.login-page {
  min-height: 100vh;
  display: flex;
  background: #000;
}

/* Left Side - Branding */
.login-branding {
  flex: 1;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.brand-content {
  max-width: 400px;
}

.brand-logo {
  font-size: 64px;
  color: #ff4500;
  margin-bottom: 16px;
}

.brand-name {
  font-size: 48px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 4px;
  margin-bottom: 12px;
}

.brand-desc {
  font-size: 16px;
  color: #888;
  margin-bottom: 48px;
  font-family: 'Space Grotesk', sans-serif;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #fff;
  font-size: 14px;
}

.feature-icon {
  font-size: 14px;
  font-weight: 700;
  color: #ff4500;
}

/* Right Side - Login Form */
.login-form-section {
  width: 480px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-card {
  width: 100%;
  max-width: 360px;
}

.card-header {
  margin-bottom: 32px;
}

.card-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #000;
  letter-spacing: 2px;
  margin: 0 0 8px 0;
}

.card-subtitle {
  font-size: 13px;
  color: #666;
  font-family: 'Space Grotesk', sans-serif;
  margin: 0;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 10px;
  font-weight: 600;
  color: #666;
  letter-spacing: 1px;
}

.form-group input {
  padding: 14px 16px;
  border: 2px solid #ccc;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  transition: border-color 0.15s;
}

.form-group input:focus {
  outline: none;
  border-color: #ff4500;
}

.form-group input::placeholder {
  color: #999;
}

/* Button */
.btn-login {
  padding: 14px;
  background: #000;
  border: 2px solid #000;
  color: #fff;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.15s;
  margin-top: 8px;
}

.btn-login:hover:not(:disabled) {
  background: #ff4500;
  border-color: #ff4500;
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Error */
.error-box {
  padding: 12px;
  background: #fff5f5;
  border: 2px solid #ff4500;
  color: #ff4500;
  font-size: 11px;
  text-align: center;
}

/* Demo Box */
.demo-box {
  margin-top: 24px;
  padding: 16px;
  background: #f8f8f8;
  border: 2px solid #ccc;
}

.demo-label {
  font-size: 9px;
  font-weight: 600;
  color: #666;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.demo-creds {
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  color: #333;
}

/* Auth Switch */
.auth-switch {
  margin-top: 24px;
  text-align: center;
  font-size: 12px;
  color: #666;
}

.auth-switch a {
  color: #ff4500;
  text-decoration: none;
  font-weight: 600;
}

.auth-switch a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 900px) {
  .login-page {
    flex-direction: column;
  }
  
  .login-branding {
    padding: 32px;
    min-height: 200px;
  }
  
  .brand-content {
    text-align: center;
  }
  
  .brand-features {
    align-items: center;
  }
  
  .login-form-section {
    width: 100%;
  }
}
</style>