<template>
  <div class="page-container">
    <h1>Analytics</h1>
    
    <div class="insights-section">
      <h2>Spending Insights</h2>
      <div v-if="insights" class="insights-grid">
        <div class="insight-card">
          <h3>Total Expenses</h3>
          <p class="value">${{ (insights.total_expenses || 0).toLocaleString() }}</p>
        </div>
        <div class="insight-card">
          <h3>Transactions</h3>
          <p class="value">{{ insights.transaction_count || 0 }}</p>
        </div>
        <div class="insight-card">
          <h3>Average Expense</h3>
          <p class="value">${{ (insights.average_expense || 0).toFixed(2) }}</p>
        </div>
        <div class="insight-card">
          <h3>Top Category</h3>
          <p class="value">{{ insights.top_category || 'N/A' }}</p>
        </div>
      </div>
      
      <div v-if="insights?.insights?.length" class="ai-insights">
        <h3>AI Insights</h3>
        <ul>
          <li v-for="(insight, i) in insights.insights" :key="i">{{ insight }}</li>
        </ul>
      </div>
    </div>
    
    <div class="chart-section">
      <h2>Spending by Category</h2>
      <div v-if="insights?.category_breakdown" class="category-chart">
        <div v-for="(amount, cat) in insights.category_breakdown" :key="cat" class="category-bar">
          <span class="cat-name">{{ cat }}</span>
          <div class="bar-container">
            <div class="bar" :style="{ width: (amount / maxCategory * 100) + '%' }"></div>
          </div>
          <span class="cat-amount">${{ amount.toFixed(0) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const insights = ref(null)

const maxCategory = computed(() => {
  if (!insights.value?.category_breakdown) return 1
  return Math.max(...Object.values(insights.value.category_breakdown))
})

const loadInsights = async () => {
  try {
    const now = new Date()
    const startDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`
    const endDate = now.toISOString().split('T')[0]
    
    const res = await api.get(`/api/financial/analytics/insights?start_date=${startDate}&end_date=${endDate}`)
    insights.value = res.data.data
  } catch (err) {
    console.error('Failed to load insights:', err)
  }
}

onMounted(loadInsights)
</script>

<style scoped>
.page-container { padding: 2rem; }
h1 { margin-bottom: 2rem; }
.insights-section, .chart-section { background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
h2 { margin: 0 0 1.5rem; color: #333; }
.insights-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; }
.insight-card { text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; }
.insight-card h3 { margin: 0 0 0.5rem; color: #666; font-size: 0.9rem; }
.insight-card .value { margin: 0; font-size: 1.5rem; font-weight: 700; color: #333; }
.ai-insights { margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #eee; }
.ai-insights h3 { color: #667eea; margin-bottom: 1rem; }
.ai-insights ul { margin: 0; padding-left: 1.5rem; }
.ai-insights li { margin-bottom: 0.5rem; color: #666; }
.category-chart { display: flex; flex-direction: column; gap: 0.75rem; }
.category-bar { display: flex; align-items: center; gap: 1rem; }
.cat-name { width: 120px; color: #333; font-size: 0.9rem; }
.bar-container { flex: 1; height: 24px; background: #eee; border-radius: 4px; overflow: hidden; }
.bar { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); }
.cat-amount { width: 80px; text-align: right; color: #666; }
</style>