<template>
  <div class="layout">
    <!-- Header -->
    <header class="header">
      <div class="brand">
        <span class="brand-square">■</span>
        <span class="brand-name">FINVEE</span>
      </div>
      
      
      
      <nav class="header-nav">
        <router-link to="/" class="nav-link">HOME</router-link>
        <span class="nav-sep">|</span>
        <span class="nav-link active">DASHBOARD</span>
        <span class="nav-sep">|</span>
        <span class="nav-user">{{ user?.username || 'GUEST' }}</span>
        <button @click="logout" class="btn-logout">[X]</button>
      </nav>
    </header>

    <div class="body">
      <!-- Sidebar - ALL MENU ALWAYS VISIBLE -->
      <aside class="sidebar">
        <div class="sidebar-label">■ ALL_MENU</div>
        
        <!-- Financial Section -->
        <router-link to="/financial/accounts" class="nav-item group-header">
          <span class="nav-icon">[$]</span>
          <span class="nav-text">FINANCIAL</span>
        </router-link>
        <router-link to="/financial/accounts" class="nav-item"> <span class="nav-icon">[B]</span> <span class="nav-text">Accounts</span> </router-link>
        <router-link to="/financial/transactions" class="nav-item"> <span class="nav-icon">[T]</span> <span class="nav-text">Transactions</span> </router-link>
        <router-link to="/financial/budgets" class="nav-item"> <span class="nav-icon">[P]</span> <span class="nav-text">Budgets</span> </router-link>
        <router-link to="/financial/analytics" class="nav-item"> <span class="nav-icon">[A]</span> <span class="nav-text">Analytics</span> </router-link>
        <router-link to="/financial/fraud" class="nav-item"> <span class="nav-icon">[F]</span> <span class="nav-text">Fraud Detection</span> </router-link>

        <div class="sidebar-divider"></div>
        
        <!-- Learning Section -->
        <router-link to="/learning/courses" class="nav-item group-header">
          <span class="nav-icon">[#]</span>
          <span class="nav-text">LEARNING</span>
        </router-link>
        <router-link to="/learning/courses" class="nav-item"> <span class="nav-icon">[C]</span> <span class="nav-text">Courses</span> </router-link>
        <router-link to="/learning/enrollments" class="nav-item"> <span class="nav-icon">[E]</span> <span class="nav-text">Enrollments</span> </router-link>
        <router-link to="/learning/tutoring" class="nav-item"> <span class="nav-icon">[S]</span> <span class="nav-text">AI Tutoring</span> </router-link>
        <router-link to="/learning/progress" class="nav-item"> <span class="nav-icon">[R]</span> <span class="nav-text">Progress</span> </router-link>

        <div class="sidebar-divider"></div>
        
        <!-- Simulation Section -->
        <router-link to="/process/new" class="nav-item group-header">
          <span class="nav-icon">[S]</span>
          <span class="nav-text">SIMULATION</span>
        </router-link>
        <router-link to="/process/new" class="nav-item"> <span class="nav-icon">[+]</span> <span class="nav-text">New Project</span> </router-link>
        <div class="nav-item" @click="goToRecent"> <span class="nav-icon">[R]</span> <span class="nav-text">Recent</span> </div>
        <router-link to="/report/demo" class="nav-item"> <span class="nav-icon">[D]</span> <span class="nav-text">Demo Report</span> </router-link>
      </aside>

      <!-- Main Content - ALL MODULES STATS -->
      <main class="main">
        <div class="tab-header">
          <h1 class="tab-title">/ DASHBOARD</h1>
          <span class="tab-time">{{ currentTime }}</span>
        </div>

        <!-- FINANCIAL STATS -->
        <div class="stats-section">
          <div class="section-label">■ FINANCIAL</div>
          <div class="stats-row">
            <div class="stat-card large">
              <div class="stat-name">TOTAL_BALANCE</div>
              <div class="stat-val">{{ formatCurrency(totalBalance) }}</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">INCOME_MONTH</div>
              <div class="stat-val pos">+{{ formatCurrency(monthlyIncome) }}</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">EXPENSE_MONTH</div>
              <div class="stat-val neg">-{{ formatCurrency(monthlyExpenses) }}</div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- LEARNING STATS -->
        <div class="stats-section">
          <div class="section-label">■ LEARNING</div>
          <div class="stats-row">
            <div class="stat-card large">
              <div class="stat-name">ENROLLED</div>
              <div class="stat-val">{{ enrollments.length }}</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">COMPLETED</div>
              <div class="stat-val done">{{ completedCourses }}</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">IN_PROGRESS</div>
              <div class="stat-val prog">{{ inProgressCourses }}</div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- SIMULATION STATS -->
        <div class="stats-section">
          <div class="section-label">■ SWARM_INTELLIGENCE</div>
          <div class="stats-row">
            <div class="stat-card large">
              <div class="stat-name">AGENTS</div>
              <div class="stat-val">1000+</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">STATUS</div>
              <div class="stat-val">ACTIVE</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">PREDICTION</div>
              <div class="stat-val done">ENABLED</div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Quick Links -->
        <div class="section-label">■ QUICK_LINKS</div>
        <div class="actions-grid">
          <router-link to="/financial/accounts" class="action-card"> <span class="action-icon">[B]</span> <div class="action-info"> <div class="action-title">ACCOUNTS</div> <div class="action-desc">Manage bank accounts</div> </div> </router-link>
          <router-link to="/financial/transactions" class="action-card"> <span class="action-icon">[T]</span> <div class="action-info"> <div class="action-title">TRANSACTIONS</div> <div class="action-desc">Track income & expense</div> </div> </router-link>
          <router-link to="/financial/budgets" class="action-card"> <span class="action-icon">[P]</span> <div class="action-info"> <div class="action-title">BUDGETS</div> <div class="action-desc">Plan monthly spending</div> </div> </router-link>
          <router-link to="/financial/analytics" class="action-card"> <span class="action-icon">[A]</span> <div class="action-info"> <div class="action-title">ANALYTICS</div> <div class="action-desc">View financial insights</div> </div> </router-link>
          <router-link to="/financial/fraud" class="action-card"> <span class="action-icon">[F]</span> <div class="action-info"> <div class="action-title">FRAUD_DETECTION</div> <div class="action-desc">AI-powered security</div> </div> </router-link>
          <router-link to="/learning/courses" class="action-card"> <span class="action-icon">[C]</span> <div class="action-info"> <div class="action-title">COURSES</div> <div class="action-desc">Browse all courses</div> </div> </router-link>
          <router-link to="/learning/enrollments" class="action-card"> <span class="action-icon">[E]</span> <div class="action-info"> <div class="action-title">ENROLLMENTS</div> <div class="action-desc">View enrollments</div> </div> </router-link>
          <router-link to="/learning/tutoring" class="action-card"> <span class="action-icon">[S]</span> <div class="action-info"> <div class="action-title">AI_TUTORING</div> <div class="action-desc">Chat with AI tutor</div> </div> </router-link>
          <router-link to="/learning/progress" class="action-card"> <span class="action-icon">[R]</span> <div class="action-info"> <div class="action-title">PROGRESS</div> <div class="action-desc">Track learning journey</div> </div> </router-link>
          <router-link to="/process/new" class="action-card"> <span class="action-icon">[+]</span> <div class="action-info"> <div class="action-title">NEW_PROJECT</div> <div class="action-desc">Start simulation</div> </div> </router-link>
          <router-link to="/report/demo" class="action-card"> <span class="action-icon">[D]</span> <div class="action-info"> <div class="action-title">DEMO_REPORT</div> <div class="action-desc">View sample prediction</div> </div> </router-link>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const activeTab = ref('financial')
const user = ref(null)
const accounts = ref([])
const transactions = ref([])
const budgets = ref([])
const enrollments = ref([])
const sessions = ref([])
const currentTime = ref('')

const updateTime = () => { currentTime.value = new Date().toISOString().slice(0, 19).replace('T', ' ') }
let timeInterval
onMounted(() => { updateTime(); timeInterval = setInterval(updateTime, 1000); loadData() })
onUnmounted(() => clearInterval(timeInterval))

const formatCurrency = (amount) => '$' + (amount || 0).toLocaleString()

const totalBalance = computed(() => accounts.value.reduce((sum, acc) => sum + acc.balance, 0))
const monthlyIncome = computed(() => {
  const now = new Date()
  const thisMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  return transactions.value.filter(t => t.type === 'income' && t.date.startsWith(thisMonth)).reduce((sum, t) => sum + t.amount, 0)
})
const monthlyExpenses = computed(() => {
  const now = new Date()
  const thisMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  return transactions.value.filter(t => t.type === 'expense' && t.date.startsWith(thisMonth)).reduce((sum, t) => sum + t.amount, 0)
})

const completedCourses = computed(() => enrollments.value.filter(e => e.status === 'completed').length)
const inProgressCourses = computed(() => enrollments.value.filter(e => e.status === 'in_progress').length)

const logout = () => { localStorage.removeItem('token'); localStorage.removeItem('user'); router.push('/login') }
const goToRecent = () => { router.push('/process/new') }

const loadData = async () => {
  const userStr = localStorage.getItem('user')
  if (userStr) user.value = JSON.parse(userStr)
  
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
  } catch (err) { console.error('Failed to load data:', err) }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

.layout { min-height: 100vh; background: #fff; font-family: 'JetBrains Mono', monospace; color: #000; }

.header { display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; background: #000; border-bottom: 2px solid #000; }
.brand { display: flex; align-items: center; gap: 6px; }
.brand-square { color: #ff4500; font-size: 10px; }
.brand-name { color: #fff; font-size: 14px; font-weight: 700; letter-spacing: 2px; }

.header-nav { display: flex; align-items: center; gap: 12px; margin-left: auto; }
.nav-link { color: #888; text-decoration: none; font-size: 12px; }
.nav-link:hover { color: #fff; }
.nav-link.active { color: #ff4500; }
.nav-sep { color: #444; }
.nav-user { color: #fff; font-size: 12px; }
.btn-logout { background: transparent; border: 1px solid #ff4500; color: #ff4500; padding: 4px 10px; font-family: inherit; font-size: 11px; cursor: pointer; }
.btn-logout:hover { background: #ff4500; color: #000; }

.body { display: flex; min-height: calc(100vh - 52px); }
.sidebar { width: 200px; background: #f8f8f8; border-right: 2px solid #ccc; padding: 20px 0; flex-shrink: 0; }
.sidebar-label { font-size: 10px; font-weight: 700; color: #666; padding: 0 16px; margin-bottom: 12px; letter-spacing: 1px; }
.sidebar-divider { height: 2px; background: #ddd; margin: 16px; }
.nav-item { display: flex; align-items: center; gap: 10px; width: calc(100% - 32px); margin: 0 16px; padding: 10px 12px; background: transparent; border: none; border-left: 2px solid transparent; color: #333; font-family: inherit; font-size: 12px; text-decoration: none; cursor: pointer; transition: all 0.15s; }
.nav-item:hover { background: #eee; border-left-color: #aaa; }
.nav-item.active { background: #fff; border-left-color: #ff4500; color: #ff4500; }
.nav-item.group-header { border-left: none; color: #666; font-weight: 700; font-size: 11px; letter-spacing: 1px; margin-top: 8px; }
.nav-item.group-header:hover { background: transparent; border-left: none; }
.nav-item.group-header .nav-icon { font-weight: 700; }
.nav-icon { font-size: 11px; color: #888; width: 20px; }
.nav-item:hover .nav-icon, .nav-item.active .nav-icon { color: #ff4500; }

.main { flex: 1; padding: 24px; background: #fff; }
.tab-header { display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 16px; border-bottom: 2px solid #000; margin-bottom: 24px; }
.tab-title { font-size: 20px; font-weight: 700; color: #ff4500; letter-spacing: 2px; margin: 0; }
.tab-time { font-size: 11px; color: #888; }
.tab-content { animation: fadeIn 0.2s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card.large { padding: 28px; border: 2px solid #ccc; background: #fff; }
.stat-name { font-size: 11px; font-weight: 600; color: #666; letter-spacing: 1px; margin-bottom: 12px; }
.stat-val { font-size: 32px; font-weight: 700; }
.stat-val.pos { color: #27ae60; }
.stat-val.neg { color: #ff4500; }
.stat-val.done { color: #27ae60; }
.stat-val.prog { color: #f39c12; }

.divider { height: 2px; background: #ccc; margin: 24px 0; }
.section-label { font-size: 12px; font-weight: 700; color: #666; letter-spacing: 1px; margin-bottom: 16px; }

.actions-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.action-card { display: flex; align-items: center; gap: 16px; padding: 20px; border: 2px solid #ccc; background: #fff; text-decoration: none; color: #000; transition: all 0.15s; }
.action-card:hover { border-color: #ff4500; background: #fafafa; }
.action-icon { font-size: 28px; font-weight: 700; color: #ff4500; }
.action-info { display: flex; flex-direction: column; gap: 4px; }
.action-title { font-size: 13px; font-weight: 600; letter-spacing: 1px; }
.action-desc { font-size: 11px; color: #666; }

.sim-hero { padding: 32px; border: 2px solid #000; background: #000; }
.sim-title { font-size: 36px; font-weight: 700; color: #fff; letter-spacing: 3px; margin-bottom: 16px; }
.sim-desc { font-size: 15px; color: #aaa; line-height: 1.6; }

.workflow-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
.workflow-card { padding: 24px; border: 2px solid #ccc; background: #fff; transition: all 0.15s; }
.workflow-card:hover { border-color: #ff4500; }
.step-num { font-size: 18px; font-weight: 700; color: #ff4500; margin-bottom: 12px; }
.step-name { font-size: 12px; font-weight: 600; letter-spacing: 1px; margin-bottom: 6px; }
.step-desc { font-size: 10px; color: #666; }

@media (max-width: 1200px) { .workflow-row { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 900px) { .stats-row { grid-template-columns: 1fr; } }
@media (max-width: 768px) { .sidebar { display: none; } .workflow-row { grid-template-columns: 1fr; } }
</style>