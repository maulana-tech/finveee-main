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
        <router-link to="/dashboard" class="nav-link">DASHBOARD</router-link>
        <span class="nav-sep">|</span>
        <span class="nav-link active">BUDGETS</span>
        <button @click="logout" class="btn-logout">[X]</button>
      </nav>
    </header>

    <div class="body">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-label">■ FINANCIAL</div>
        
        <router-link to="/financial/accounts" class="nav-item">
          <span class="nav-icon">[B]</span>
          <span class="nav-text">Accounts</span>
        </router-link>
        <router-link to="/financial/transactions" class="nav-item">
          <span class="nav-icon">[T]</span>
          <span class="nav-text">Transactions</span>
        </router-link>
        <router-link to="/financial/budgets" class="nav-item" :class="{ active: true }">
          <span class="nav-icon">[P]</span>
          <span class="nav-text">Budgets</span>
        </router-link>
        <router-link to="/financial/analytics" class="nav-item">
          <span class="nav-icon">[A]</span>
          <span class="nav-text">Analytics</span>
        </router-link>
        <router-link to="/financial/fraud" class="nav-item">
          <span class="nav-icon">[F]</span>
          <span class="nav-text">Fraud</span>
        </router-link>

        <div class="sidebar-divider"></div>

        <div class="sidebar-label">■ MODULES</div>
        
        <button @click="switchTab('financial')" class="nav-item">
          <span class="nav-icon">[$]</span>
          <span class="nav-text">Financial</span>
        </button>
        <button @click="switchTab('learning')" class="nav-item">
          <span class="nav-icon">[#]</span>
          <span class="nav-text">Learning</span>
        </button>
        <button @click="switchTab('simulation')" class="nav-item">
          <span class="nav-icon">[S]</span>
          <span class="nav-text">Simulation</span>
        </button>
      </aside>

      <!-- Main Content -->
      <main class="main">
        <div class="tab-header">
          <h1 class="tab-title">/ BUDGETS</h1>
          <span class="tab-time">{{ currentTime }}</span>
        </div>

        <!-- Stats -->
        <div class="stats-row">
          <div class="stat-card large">
            <div class="stat-name">TOTAL_BUDGETS</div>
            <div class="stat-val">{{ budgets.length }}</div>
          </div>
          <div class="stat-card large">
            <div class="stat-name">TOTAL_ALLOCATED</div>
            <div class="stat-val">{{ formatCurrency(totalAllocated) }}</div>
          </div>
          <div class="stat-card large">
            <div class="stat-name">TOTAL_SPENT</div>
            <div class="stat-val neg">{{ formatCurrency(totalSpent) }}</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section-label">■ BUDGETS_LIST</div>

        <div class="card-grid">
          <div v-for="budget in budgets" :key="budget.budget_id" class="card big">
            <div class="card-top">
              <div class="card-name-lg">{{ budget.category }}</div>
              <div class="card-period">{{ budget.period }}</div>
            </div>
            <div class="card-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: getProgress(budget) + '%' }" 
                     :class="{ warning: getProgress(budget) > 80, over: getProgress(budget) > 100 }"></div>
              </div>
              <div class="progress-text">
                <span>${{ budget.spent.toFixed(2) }}</span>
                <span>/ ${{ budget.amount }}</span>
                <span class="progress-pct">{{ getProgress(budget).toFixed(0) }}%</span>
              </div>
            </div>
          </div>

          <div v-if="budgets.length === 0" class="empty-card">
            <div class="empty-icon">[P]</div>
            <div class="empty-text">No budgets yet</div>
            <button @click="showAddModal = true" class="btn-primary">+ ADD_BUDGET</button>
          </div>
        </div>

        <button @click="showAddModal = true" class="btn-add-float">+</button>
      </main>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2>NEW_BUDGET</h2>
          <button @click="showAddModal = false" class="modal-close">[X]</button>
        </div>
        <form @submit.prevent="createBudget" class="form">
          <div class="form-group">
            <label>CATEGORY</label>
            <select v-model="newBudget.category" required>
              <option v-for="cat in categories" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>AMOUNT</label>
            <input v-model.number="newBudget.amount" type="number" step="0.01" required />
          </div>
          <div class="form-group">
            <label>PERIOD</label>
            <select v-model="newBudget.period" required>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
            </select>
          </div>
          <div class="form-group">
            <label>START_DATE</label>
            <input v-model="newBudget.start_date" type="date" required />
          </div>
          <div class="form-group">
            <label>END_DATE</label>
            <input v-model="newBudget.end_date" type="date" required />
          </div>
          <div class="form-actions">
            <button type="button" @click="showAddModal = false" class="btn-cancel">CANCEL</button>
            <button type="submit" class="btn-submit">CREATE</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()

const budgets = ref([])
const showAddModal = ref(false)
const currentTime = ref('')
const categories = ['Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 'Bills & Utilities', 'Health', 'Education', 'Travel']
const newBudget = ref({ category: 'Food & Dining', amount: 0, period: 'monthly', start_date: '', end_date: '' })

const totalAllocated = computed(() => budgets.value.reduce((sum, b) => sum + b.amount, 0))
const totalSpent = computed(() => budgets.value.reduce((sum, b) => sum + b.spent, 0))

const updateTime = () => { currentTime.value = new Date().toISOString().slice(0, 19).replace('T', ' ') }
let timeInterval
onMounted(() => { updateTime(); timeInterval = setInterval(updateTime, 1000) })
onUnmounted(() => clearInterval(timeInterval))

const formatCurrency = (amount) => '$' + (amount || 0).toLocaleString()
const getProgress = (b) => Math.min((b.spent / b.amount) * 100, 100)
const switchTab = (tab) => router.push('/dashboard?tab=' + tab)
const logout = () => { localStorage.removeItem('token'); localStorage.removeItem('user'); router.push('/login') }

const loadBudgets = async () => {
  try {
    const res = await api.get('/api/financial/budgets')
    budgets.value = res.data.data || []
  } catch (err) { console.error('Failed to load budgets:', err) }
}

const createBudget = async () => {
  try {
    await api.post('/api/financial/budgets', newBudget.value)
    showAddModal.value = false
    loadBudgets()
  } catch (err) { alert('Failed to create budget') }
}

onMounted(() => {
  const now = new Date()
  newBudget.value.start_date = now.toISOString().split('T')[0]
  const end = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  newBudget.value.end_date = end.toISOString().split('T')[0]
  loadBudgets()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

.layout { min-height: 100vh; background: #fff; font-family: 'JetBrains Mono', monospace; color: #000; }
.header { display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; background: #000; border-bottom: 2px solid #000; }
.brand { display: flex; align-items: center; gap: 6px; }
.brand-square { color: #ff4500; font-size: 10px; }
.brand-name { color: #fff; font-size: 14px; font-weight: 700; letter-spacing: 2px; }
.header-nav { display: flex; align-items: center; gap: 12px; }
.nav-link { color: #888; text-decoration: none; font-size: 12px; }
.nav-link:hover { color: #fff; }
.nav-link.active { color: #ff4500; }
.nav-sep { color: #444; }
.btn-logout { background: transparent; border: 1px solid #ff4500; color: #ff4500; padding: 4px 10px; font-family: inherit; font-size: 11px; cursor: pointer; }
.btn-logout:hover { background: #ff4500; color: #000; }

.body { display: flex; min-height: calc(100vh - 52px); }
.sidebar { width: 200px; background: #f8f8f8; border-right: 2px solid #ccc; padding: 20px 0; flex-shrink: 0; }
.sidebar-label { font-size: 10px; font-weight: 700; color: #666; padding: 0 16px; margin-bottom: 12px; letter-spacing: 1px; }
.sidebar-divider { height: 2px; background: #ddd; margin: 16px; }
.nav-item { display: flex; align-items: center; gap: 10px; width: calc(100% - 32px); margin: 0 16px; padding: 10px 12px; background: transparent; border: none; border-left: 2px solid transparent; color: #333; font-family: inherit; font-size: 12px; text-decoration: none; cursor: pointer; transition: all 0.15s; }
.nav-item:hover { background: #eee; border-left-color: #aaa; }
.nav-item.active { background: #fff; border-left-color: #ff4500; color: #ff4500; }
.nav-icon { font-size: 11px; color: #888; width: 20px; }
.nav-item:hover .nav-icon, .nav-item.active .nav-icon { color: #ff4500; }

.main { flex: 1; padding: 24px; background: #fff; }
.tab-header { display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 16px; border-bottom: 2px solid #000; margin-bottom: 24px; }
.tab-title { font-size: 20px; font-weight: 700; color: #ff4500; letter-spacing: 2px; margin: 0; }
.tab-time { font-size: 11px; color: #888; }

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card.large { padding: 28px; border: 2px solid #ccc; background: #fff; }
.stat-name { font-size: 11px; font-weight: 600; color: #666; letter-spacing: 1px; margin-bottom: 12px; }
.stat-val { font-size: 32px; font-weight: 700; }
.stat-val.neg { color: #ff4500; }

.divider { height: 2px; background: #ccc; margin: 24px 0; }
.section-label { font-size: 12px; font-weight: 700; color: #666; letter-spacing: 1px; margin-bottom: 16px; }

.card-grid { display: grid; gap: 16px; }
.card.big { padding: 24px; border: 2px solid #ccc; background: #fff; transition: all 0.15s; }
.card.big:hover { border-color: #ff4500; }
.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.card-name-lg { font-size: 18px; font-weight: 600; }
.card-period { font-size: 12px; color: #666; text-transform: capitalize; }
.progress-bar { height: 14px; background: #eee; border: 1px solid #ccc; }
.progress-fill { height: 100%; background: #27ae60; transition: width 0.3s; }
.progress-fill.warning { background: #f39c12; }
.progress-fill.over { background: #ff4500; }
.progress-text { display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; color: #666; }
.progress-pct { font-weight: 700; color: #ff4500; }

.empty-card { padding: 60px; text-align: center; border: 2px solid #ccc; }
.empty-icon { font-size: 48px; color: #ccc; margin-bottom: 16px; }
.empty-text { font-size: 16px; color: #666; margin-bottom: 20px; }
.btn-primary { background: #000; border: 2px solid #000; color: #fff; padding: 12px 24px; font-family: inherit; font-size: 12px; font-weight: 600; cursor: pointer; }
.btn-primary:hover { background: #ff4500; border-color: #ff4500; }

.btn-add-float { position: fixed; bottom: 32px; right: 32px; width: 56px; height: 56px; background: #ff4500; border: 2px solid #ff4500; color: #fff; font-size: 28px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(255, 69, 0, 0.4); }
.btn-add-float:hover { background: #000; border-color: #000; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; border: 2px solid #000; width: 100%; max-width: 420px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 2px solid #ccc; }
.modal-header h2 { font-size: 14px; margin: 0; letter-spacing: 1px; }
.modal-close { background: none; border: none; color: #666; font-family: inherit; font-size: 14px; cursor: pointer; }
.form { padding: 20px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 10px; font-weight: 600; color: #666; margin-bottom: 8px; letter-spacing: 1px; }
.form-group input, .form-group select { width: 100%; padding: 14px; border: 2px solid #ccc; font-family: inherit; font-size: 14px; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: #ff4500; }
.form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 24px; }
.btn-cancel { background: #fff; border: 2px solid #ccc; color: #666; padding: 12px 24px; font-family: inherit; font-size: 12px; cursor: pointer; }
.btn-cancel:hover { border-color: #333; }
.btn-submit { background: #000; border: 2px solid #000; color: #fff; padding: 12px 24px; font-family: inherit; font-size: 12px; font-weight: 600; cursor: pointer; }
.btn-submit:hover { background: #ff4500; border-color: #ff4500; }

@media (max-width: 768px) { .sidebar { display: none; } .stats-row { grid-template-columns: 1fr; } }
</style>