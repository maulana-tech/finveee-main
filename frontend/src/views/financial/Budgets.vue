<template>
  <div class="page-container">
    <header class="page-header">
      <h1>Budgets</h1>
      <button @click="showAddModal = true" class="btn-primary">+ Add Budget</button>
    </header>
    
    <div class="budgets-list">
      <div v-for="budget in budgets" :key="budget.budget_id" class="budget-card">
        <div class="budget-info">
          <h3>{{ budget.category }}</h3>
          <p>{{ budget.period }}</p>
        </div>
        <div class="budget-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: getProgress(budget) + '%' }" 
                 :class="{ warning: getProgress(budget) > 80, danger: getProgress(budget) > 100 }"></div>
          </div>
          <div class="progress-text">
            <span>${{ budget.spent.toFixed(2) }} / ${{ budget.amount }}</span>
            <span>{{ getProgress(budget).toFixed(0) }}%</span>
          </div>
        </div>
      </div>
      
      <div v-if="budgets.length === 0" class="empty-state">
        <p>No budgets yet. Create one to track your spending!</p>
      </div>
    </div>
    
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <h2>Create Budget</h2>
        <form @submit.prevent="createBudget">
          <div class="form-group">
            <label>Category</label>
            <select v-model="newBudget.category" required>
              <option v-for="cat in categories" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Amount</label>
            <input v-model.number="newBudget.amount" type="number" step="0.01" required />
          </div>
          <div class="form-group">
            <label>Period</label>
            <select v-model="newBudget.period" required>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
            </select>
          </div>
          <div class="form-group">
            <label>Start Date</label>
            <input v-model="newBudget.start_date" type="date" required />
          </div>
          <div class="form-group">
            <label>End Date</label>
            <input v-model="newBudget.end_date" type="date" required />
          </div>
          <div class="form-actions">
            <button type="button" @click="showAddModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Create</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const budgets = ref([])
const showAddModal = ref(false)
const categories = ['Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 'Bills & Utilities', 'Health', 'Education', 'Travel']
const newBudget = ref({ category: 'Food & Dining', amount: 0, period: 'monthly', start_date: '', end_date: '' })

const getProgress = (b) => Math.min((b.spent / b.amount) * 100, 100)

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
.page-container { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.budgets-list { display: grid; gap: 1rem; }
.budget-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.budget-info h3 { margin: 0; color: #333; }
.budget-info p { margin: 0.25rem 0 1rem; color: #666; font-size: 0.9rem; text-transform: capitalize; }
.progress-bar { height: 8px; background: #eee; border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; background: #27ae60; transition: width 0.3s; }
.progress-fill.warning { background: #f39c12; }
.progress-fill.danger { background: #e74c3c; }
.progress-text { display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.9rem; color: #666; }
.empty-state { text-align: center; padding: 2rem; color: #666; }
.btn-primary { background: #667eea; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; }
.btn-secondary { background: #ddd; color: #333; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 100%; max-width: 400px; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.form-group input, .form-group select { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; }
.form-actions { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>