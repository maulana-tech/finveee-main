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
        <span class="nav-link active">ANALYTICS</span>
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
        <router-link to="/financial/analytics" class="nav-item" :class="{ active: true }">
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
          <h1 class="tab-title">/ ANALYTICS</h1>
          <span class="tab-time">{{ currentTime }}</span>
        </div>

        <!-- Insights -->
        <div v-if="insights" class="tab-content">
          <div class="stats-row">
            <div class="stat-card large">
              <div class="stat-name">TOTAL_EXPENSES</div>
              <div class="stat-val">{{ formatCurrency(insights.total_expenses || 0) }}</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">TRANSACTIONS</div>
              <div class="stat-val">{{ insights.transaction_count || 0 }}</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">AVG_EXPENSE</div>
              <div class="stat-val">{{ formatCurrency(insights.average_expense || 0) }}</div>
            </div>
            <div class="stat-card large">
              <div class="stat-name">TOP_CATEGORY</div>
              <div class="stat-val">{{ insights.top_category || 'N/A' }}</div>
            </div>
          </div>

          <div class="divider"></div>

          <div class="section-label">■ SPENDING_BY_CATEGORY</div>

          <div class="card-grid">
            <div v-for="(amount, cat) in insights.category_breakdown" :key="cat" class="card big">
              <div class="card-name-lg">{{ cat }}</div>
              <div class="card-bar">
                <div class="bar-fill" :style="{ width: (amount / maxCategory * 100) + '%' }"></div>
              </div>
              <div class="card-val-lg">{{ formatCurrency(amount) }}</div>
            </div>
          </div>

          <div v-if="insights?.insights?.length" class="divider"></div>

          <div v-if="insights?.insights?.length" class="section-label">■ AI_INSIGHTS</div>
          
          <div v-if="insights?.insights?.length" class="ai-box">
            <ul class="ai-list">
              <li v-for="(insight, i) in insights.insights" :key="i">{{ insight }}</li>
            </ul>
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
const insights = ref(null)
const currentTime = ref('')

const maxCategory = computed(() => {
  if (!insights.value?.category_breakdown) return 1
  return Math.max(...Object.values(insights.value.category_breakdown))
})

const updateTime = () => { currentTime.value = new Date().toISOString().slice(0, 19).replace('T', ' ') }
let timeInterval
onMounted(() => { updateTime(); timeInterval = setInterval(updateTime, 1000) })
onUnmounted(() => clearInterval(timeInterval))

const formatCurrency = (amount) => '$' + (amount || 0).toLocaleString()
const switchTab = (tab) => router.push('/dashboard?tab=' + tab)
const logout = () => { localStorage.removeItem('token'); localStorage.removeItem('user'); router.push('/login') }

const loadInsights = async () => {
  try {
    const now = new Date()
    const startDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`
    const endDate = now.toISOString().split('T')[0]
    const res = await api.get(`/api/financial/analytics/insights?start_date=${startDate}&end_date=${endDate}`)
    insights.value = res.data.data
  } catch (err) { console.error('Failed to load insights:', err) }
}

onMounted(loadInsights)
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

.tab-content { animation: fadeIn 0.2s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card.large { padding: 28px; border: 2px solid #ccc; background: #fff; }
.stat-name { font-size: 11px; font-weight: 600; color: #666; letter-spacing: 1px; margin-bottom: 12px; }
.stat-val { font-size: 28px; font-weight: 700; }

.divider { height: 2px; background: #ccc; margin: 24px 0; }
.section-label { font-size: 12px; font-weight: 700; color: #666; letter-spacing: 1px; margin-bottom: 16px; }

.card-grid { display: grid; gap: 16px; }
.card.big { padding: 20px; border: 2px solid #ccc; background: #fff; transition: all 0.15s; }
.card.big:hover { border-color: #ff4500; }
.card-name-lg { font-size: 14px; font-weight: 600; margin-bottom: 12px; }
.card-bar { height: 20px; background: #eee; border: 1px solid #ccc; margin-bottom: 8px; }
.bar-fill { height: 100%; background: #ff4500; transition: width 0.3s; }
.card-val-lg { font-size: 18px; font-weight: 700; text-align: right; }

.ai-box { padding: 24px; border: 2px solid #000; background: #000; }
.ai-list { margin: 0; padding-left: 20px; color: #aaa; font-size: 13px; line-height: 1.8; }

@media (max-width: 900px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .sidebar { display: none; } }
</style>