<template>
  <div class="dashboard">
    <header class="header">
      <h1>Finvee</h1>
      <div class="user-info">
        <span>{{ user?.username }}</span>
        <button @click="logout">Logout</button>
      </div>
    </header>
    
    <div class="nav-tabs">
      <button 
        :class="{ active: activeTab === 'financial' }" 
        @click="activeTab = 'financial'"
      >
        💰 Financial
      </button>
      <button 
        :class="{ active: activeTab === 'learning' }" 
        @click="activeTab = 'learning'"
      >
        📚 Learning
      </button>
    </div>
    
    <!-- Financial Dashboard -->
    <div v-if="activeTab === 'financial'" class="tab-content">
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Balance</h3>
          <p class="stat-value">${{ totalBalance.toLocaleString() }}</p>
        </div>
        <div class="stat-card">
          <h3>Income (This Month)</h3>
          <p class="stat-value income">${{ monthlyIncome.toLocaleString() }}</p>
        </div>
        <div class="stat-card">
          <h3>Expenses (This Month)</h3>
          <p class="stat-value expense">${{ monthlyExpenses.toLocaleString() }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Budgets</h3>
          <p class="stat-value">{{ budgets.length }}</p>
        </div>
      </div>
      
      <div class="quick-actions">
        <h2>Quick Actions</h2>
        <div class="action-buttons">
          <router-link to="/financial/accounts" class="action-btn">
            <span class="icon">🏦</span>
            <span>Accounts</span>
          </router-link>
          <router-link to="/financial/transactions" class="action-btn">
            <span class="icon">💳</span>
            <span>Transactions</span>
          </router-link>
          <router-link to="/financial/budgets" class="action-btn">
            <span class="icon">📊</span>
            <span>Budgets</span>
          </router-link>
          <router-link to="/financial/analytics" class="action-btn">
            <span class="icon">📈</span>
            <span>Analytics</span>
          </router-link>
          <router-link to="/financial/fraud" class="action-btn">
            <span class="icon">🛡️</span>
            <span>Fraud Detection</span>
          </router-link>
        </div>
      </div>
    </div>
    
    <!-- Learning Dashboard -->
    <div v-if="activeTab === 'learning'" class="tab-content">
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Enrolled Courses</h3>
          <p class="stat-value">{{ enrollments.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Completed</h3>
          <p class="stat-value">{{ completedCourses }}</p>
        </div>
        <div class="stat-card">
          <h3>In Progress</h3>
          <p class="stat-value">{{ inProgressCourses }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Tutoring</h3>
          <p class="stat-value">{{ activeSessions }}</p>
        </div>
      </div>
      
      <div class="quick-actions">
        <h2>Quick Actions</h2>
        <div class="action-buttons">
          <router-link to="/learning/courses" class="action-btn">
            <span class="icon">📖</span>
            <span>Courses</span>
          </router-link>
          <router-link to="/learning/enrollments" class="action-btn">
            <span class="icon">🎓</span>
            <span>My Learning</span>
          </router-link>
          <router-link to="/learning/tutoring" class="action-btn">
            <span class="icon">💬</span>
            <span>AI Tutoring</span>
          </router-link>
          <router-link to="/learning/progress" class="action-btn">
            <span class="icon">📊</span>
            <span>Progress</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/index.js'

const router = useRouter()
const activeTab = ref('financial')
const user = ref(null)
const accounts = ref([])
const transactions = ref([])
const budgets = ref([])
const enrollments = ref([])
const sessions = ref([])

const totalBalance = computed(() => 
  accounts.value.reduce((sum, acc) => sum + acc.balance, 0)
)

const monthlyIncome = computed(() => {
  const now = new Date()
  const thisMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  return transactions.value
    .filter(t => t.type === 'income' && t.date.startsWith(thisMonth))
    .reduce((sum, t) => sum + t.amount, 0)
})

const monthlyExpenses = computed(() => {
  const now = new Date()
  const thisMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  return transactions.value
    .filter(t => t.type === 'expense' && t.date.startsWith(thisMonth))
    .reduce((sum, t) => sum + t.amount, 0)
})

const completedCourses = computed(() => 
  enrollments.value.filter(e => e.status === 'completed').length
)

const inProgressCourses = computed(() => 
  enrollments.value.filter(e => e.status === 'in_progress').length
)

const activeSessions = computed(() => 
  sessions.value.filter(s => s.status === 'active').length
)

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

const loadData = async () => {
  const token = localStorage.getItem('user')
  if (token) {
    user.value = JSON.parse(token)
  }
  
  try {
    const [accRes, txnRes, budRes, enrRes, sesRes] = await Promise.all([
      api.get('/api/financial/accounts'),
      api.get('/api/financial/transactions'),
      api.get('/api/financial/budgets'),
      api.get('/api/learning/enrollments'),
      api.get('/api/learning/tutoring')
    ])
    
    accounts.value = accRes.data.data || []
    transactions.value = txnRes.data.data || []
    budgets.value = budRes.data.data || []
    enrollments.value = enrRes.data.data || []
    sessions.value = sesRes.data.data || []
  } catch (err) {
    console.error('Failed to load data:', err)
  }
}

onMounted(loadData)
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f5f5;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info button {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.nav-tabs {
  display: flex;
  background: white;
  border-bottom: 1px solid #ddd;
}

.nav-tabs button {
  flex: 1;
  padding: 1rem;
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  border-bottom: 3px solid transparent;
}

.nav-tabs button.active {
  border-bottom-color: #667eea;
  color: #667eea;
  font-weight: 600;
}

.tab-content {
  padding: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-card h3 {
  margin: 0 0 0.5rem;
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.stat-value.income {
  color: #27ae60;
}

.stat-value.expense {
  color: #e74c3c;
}

.quick-actions h2 {
  margin-bottom: 1rem;
  color: #333;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  transition: all 0.3s;
}

.action-btn:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.action-btn .icon {
  font-size: 1.5rem;
}
</style>