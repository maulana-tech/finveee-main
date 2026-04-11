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
        <span class="nav-link active">FRAUD</span>
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
        <router-link to="/financial/budgets" class="nav-item">
          <span class="nav-icon">[P]</span>
          <span class="nav-text">Budgets</span>
        </router-link>
        <router-link to="/financial/analytics" class="nav-item">
          <span class="nav-icon">[A]</span>
          <span class="nav-text">Analytics</span>
        </router-link>
        <router-link to="/financial/fraud" class="nav-item" :class="{ active: true }">
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
          <h1 class="tab-title">/ FRAUD_DETECTION</h1>
          <span class="tab-time">{{ currentTime }}</span>
        </div>

        <!-- Stats -->
        <div class="stats-row">
          <div class="stat-card large">
            <div class="stat-name">ANALYZED</div>
            <div class="stat-val">{{ transactions.length }}</div>
          </div>
          <div class="stat-card large warn">
            <div class="stat-name">FLAGGED</div>
            <div class="stat-val">{{ flaggedCount }}</div>
          </div>
          <div class="stat-card large danger">
            <div class="stat-name">HIGH_RISK</div>
            <div class="stat-val">{{ highRiskCount }}</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section-label">■ TRANSACTION_ANALYSIS</div>

        <div class="card-grid">
          <div v-for="txn in transactions" :key="txn.transaction_id" 
               class="card big" :class="{ flagged: txn.is_fraudulent, 'high-risk': txn.fraud_score > 0.5 }">
            <div class="card-left">
              <div class="card-icon-lg" :class="txn.type">{{ txn.type === 'income' ? '[+]' : '[-]' }}</div>
            </div>
            <div class="card-mid">
              <div class="card-name-lg">{{ txn.description || txn.category }}</div>
              <div class="card-type-lg">{{ formatDate(txn.date) }}</div>
            </div>
            <div class="card-right">
              <div class="card-balance-lg" :class="txn.type">
                {{ txn.type === 'income' ? '+' : '-' }}${{ txn.amount.toLocaleString() }}
              </div>
              <div v-if="txn.is_fraudulent" class="fraud-tag">[FRAUD]</div>
              <div v-else class="safe-tag">[SAFE]</div>
              <div class="score-tag">Score: {{ (txn.fraud_score || 0).toFixed(2) }}</div>
            </div>
          </div>

          <div v-if="transactions.length === 0" class="empty-card">
            <div class="empty-icon">[F]</div>
            <div class="empty-text">No transactions to analyze</div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const transactions = ref([])
const currentTime = ref('')

const flaggedCount = computed(() => transactions.value.filter(t => t.is_fraudulent).length)
const highRiskCount = computed(() => transactions.value.filter(t => t.fraud_score > 0.5).length)

const updateTime = () => { currentTime.value = new Date().toISOString().slice(0, 19).replace('T', ' ') }
let timeInterval
onMounted(() => { updateTime(); timeInterval = setInterval(updateTime, 1000) })
onUnmounted(() => clearInterval(timeInterval))

const formatDate = (date) => new Date(date).toLocaleDateString()
const switchTab = (tab) => router.push('/dashboard?tab=' + tab)
const logout = () => { localStorage.removeItem('token'); localStorage.removeItem('user'); router.push('/login') }

const loadTransactions = async () => {
  try {
    const res = await api.get('/api/financial/transactions')
    transactions.value = res.data.data || []
  } catch (err) { console.error('Failed to load transactions:', err) }
}

onMounted(loadTransactions)
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
.stat-card.large.warn { border-color: #f39c12; }
.stat-card.large.danger { border-color: #ff4500; }
.stat-name { font-size: 11px; font-weight: 600; color: #666; letter-spacing: 1px; margin-bottom: 12px; }
.stat-val { font-size: 32px; font-weight: 700; }
.stat-card.large.warn .stat-val { color: #f39c12; }
.stat-card.large.danger .stat-val { color: #ff4500; }

.divider { height: 2px; background: #ccc; margin: 24px 0; }
.section-label { font-size: 12px; font-weight: 700; color: #666; letter-spacing: 1px; margin-bottom: 16px; }

.card-grid { display: grid; gap: 16px; }
.card.big { display: flex; align-items: center; padding: 24px; border: 2px solid #ccc; background: #fff; transition: all 0.15s; }
.card.big:hover { border-color: #ff4500; }
.card.big.flagged { border-color: #f39c12; background: #fffbf0; }
.card.big.high-risk { border-color: #ff4500; background: #fff5f5; }
.card-icon-lg { font-size: 32px; font-weight: 700; margin-right: 20px; }
.card-icon-lg.income { color: #27ae60; }
.card-icon-lg.expense { color: #ff4500; }
.card-mid { flex: 1; }
.card-name-lg { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
.card-type-lg { font-size: 12px; color: #666; }
.card-right { text-align: right; }
.card-balance-lg { font-size: 28px; font-weight: 700; }
.card-balance-lg.income { color: #27ae60; }
.card-balance-lg.expense { color: #ff4500; }
.fraud-tag { font-size: 10px; color: #ff0000; font-weight: 600; margin-top: 6px; }
.safe-tag { font-size: 10px; color: #27ae60; font-weight: 600; margin-top: 6px; }
.score-tag { font-size: 10px; color: #666; margin-top: 4px; }

.empty-card { padding: 60px; text-align: center; border: 2px solid #ccc; }
.empty-icon { font-size: 48px; color: #ccc; margin-bottom: 16px; }
.empty-text { font-size: 16px; color: #666; }

@media (max-width: 768px) { .sidebar { display: none; } .stats-row { grid-template-columns: 1fr; } }
</style>