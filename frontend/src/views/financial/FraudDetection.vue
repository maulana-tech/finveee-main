<template>
  <div class="page-container">
    <h1>Fraud Detection</h1>
    <p class="subtitle">AI-powered transaction monitoring and alerts</p>
    
    <div class="stats-row">
      <div class="stat-card">
        <h3>Total Analyzed</h3>
        <p>{{ transactions.length }}</p>
      </div>
      <div class="stat-card warning">
        <h3>Flagged</h3>
        <p>{{ flaggedCount }}</p>
      </div>
      <div class="stat-card danger">
        <h3>High Risk</h3>
        <p>{{ highRiskCount }}</p>
      </div>
    </div>
    
    <div class="transactions-list">
      <h2>Transaction Analysis</h2>
      <div v-for="txn in transactions" :key="txn.transaction_id" 
           class="txn-card" :class="{ flagged: txn.is_fraudulent, 'high-risk': txn.fraud_score > 0.5 }">
        <div class="txn-main">
          <div class="txn-info">
            <span class="amount" :class="txn.type">{{ txn.type === 'income' ? '+' : '-' }}${{ txn.amount.toLocaleString() }}</span>
            <span class="desc">{{ txn.description || txn.category }}</span>
            <span class="date">{{ formatDate(txn.date) }}</span>
          </div>
          <div class="txn-status">
            <div v-if="txn.is_fraudulent" class="status-badge danger">
              ⚠️ Fraud Detected
            </div>
            <div v-else class="status-badge safe">
              ✓ Safe
            </div>
            <div class="fraud-score">
              Score: {{ (txn.fraud_score || 0).toFixed(2) }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="transactions.length === 0" class="empty-state">
        <p>No transactions to analyze.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const transactions = ref([])

const flaggedCount = computed(() => transactions.value.filter(t => t.is_fraudulent).length)
const highRiskCount = computed(() => transactions.value.filter(t => t.fraud_score > 0.5).length)

const formatDate = (date) => new Date(date).toLocaleDateString()

const loadTransactions = async () => {
  try {
    const res = await api.get('/api/financial/transactions')
    transactions.value = res.data.data || []
  } catch (err) {
    console.error('Failed to load transactions:', err)
  }
}

onMounted(loadTransactions)
</script>

<style scoped>
.page-container { padding: 2rem; }
h1 { margin-bottom: 0.5rem; }
.subtitle { color: #666; margin-bottom: 2rem; }
.stats-row { display: flex; gap: 1rem; margin-bottom: 2rem; }
.stat-card { flex: 1; background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.stat-card h3 { margin: 0 0 0.5rem; color: #666; font-size: 0.9rem; }
.stat-card p { margin: 0; font-size: 2rem; font-weight: 700; }
.stat-card.warning p { color: #f39c12; }
.stat-card.danger p { color: #e74c3c; }
.transactions-list { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.transactions-list h2 { margin: 0 0 1.5rem; }
.txn-card { padding: 1rem; border: 1px solid #eee; border-radius: 8px; margin-bottom: 0.75rem; }
.txn-card.flagged { border-color: #f39c12; background: #fffbf0; }
.txn-card.high-risk { border-color: #e74c3c; background: #fff5f5; }
.txn-main { display: flex; justify-content: space-between; align-items: center; }
.txn-info { display: flex; flex-direction: column; gap: 0.25rem; }
.txn-info .amount { font-size: 1.2rem; font-weight: 700; }
.txn-info .amount.income { color: #27ae60; }
.txn-info .amount.expense { color: #e74c3c; }
.txn-info .desc { color: #333; }
.txn-info .date { color: #999; font-size: 0.85rem; }
.tx-status { text-align: right; }
.status-badge { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; }
.status-badge.danger { background: #fee; color: #e74c3c; }
.status-badge.safe { background: #efe; color: #27ae60; }
.fraud-score { font-size: 0.8rem; color: #666; margin-top: 0.25rem; }
.empty-state { text-align: center; padding: 2rem; color: #666; }
</style>