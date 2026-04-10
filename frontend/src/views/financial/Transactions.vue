<template>
  <div class="page-container">
    <header class="page-header">
      <h1>Transactions</h1>
      <button @click="showAddModal = true" class="btn-primary">+ Add Transaction</button>
    </header>
    
    <div class="filters">
      <select v-model="filterType">
        <option value="">All Types</option>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>
      <select v-model="filterAccount">
        <option value="">All Accounts</option>
        <option v-for="acc in accounts" :key="acc.account_id" :value="acc.account_id">{{ acc.name }}</option>
      </select>
    </div>
    
    <div class="transactions-list">
      <div v-for="txn in filteredTransactions" :key="txn.transaction_id" 
           class="transaction-card" :class="txn.type">
        <div class="txn-info">
          <span class="txn-category">{{ txn.category }}</span>
          <span class="txn-desc">{{ txn.description }}</span>
          <span class="txn-date">{{ formatDate(txn.date) }}</span>
        </div>
        <div class="txn-amount">
          <span :class="txn.type">{{ txn.type === 'income' ? '+' : '-' }}${{ txn.amount.toLocaleString() }}</span>
          <span v-if="txn.is_fraudulent" class="fraud-badge">⚠️ Fraud</span>
        </div>
      </div>
      
      <div v-if="filteredTransactions.length === 0" class="empty-state">
        <p>No transactions found.</p>
      </div>
    </div>
    
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <h2>Add Transaction</h2>
        <form @submit.prevent="createTransaction">
          <div class="form-group">
            <label>Account</label>
            <select v-model="newTxn.account_id" required>
              <option v-for="acc in accounts" :key="acc.account_id" :value="acc.account_id">{{ acc.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Type</label>
            <select v-model="newTxn.type" required>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </div>
          <div class="form-group">
            <label>Amount</label>
            <input v-model.number="newTxn.amount" type="number" step="0.01" required />
          </div>
          <div class="form-group">
            <label>Category</label>
            <select v-model="newTxn.category" required>
              <option v-if="newTxn.type === 'expense'" v-for="cat in expenseCategories" :value="cat">{{ cat }}</option>
              <option v-else v-for="cat in incomeCategories" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Description</label>
            <input v-model="newTxn.description" type="text" />
          </div>
          <div class="form-group">
            <label>Date</label>
            <input v-model="newTxn.date" type="date" required />
          </div>
          <div class="form-actions">
            <button type="button" @click="showAddModal = false" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Add</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const transactions = ref([])
const accounts = ref([])
const filterType = ref('')
const filterAccount = ref('')
const showAddModal = ref(false)
const newTxn = ref({ account_id: '', type: 'expense', amount: 0, category: '', description: '', date: new Date().toISOString().split('T')[0] })

const expenseCategories = ['Food & Dining', 'Transportation', 'Shopping', 'Entertainment', 'Bills & Utilities', 'Health', 'Education', 'Travel', 'Other']
const incomeCategories = ['Salary', 'Investment', 'Gift', 'Business', 'Refund', 'Other']

const filteredTransactions = computed(() => {
  return transactions.value.filter(t => {
    if (filterType.value && t.type !== filterType.value) return false
    if (filterAccount.value && t.account_id !== filterAccount.value) return false
    return true
  })
})

const formatDate = (date) => new Date(date).toLocaleDateString()

const loadData = async () => {
  try {
    const [txnRes, accRes] = await Promise.all([api.get('/api/financial/transactions'), api.get('/api/financial/accounts')])
    transactions.value = txnRes.data.data || []
    accounts.value = accRes.data.data || []
    if (accounts.value.length && !newTxn.value.account_id) newTxn.value.account_id = accounts.value[0].account_id
  } catch (err) { console.error('Failed to load data:', err) }
}

const createTransaction = async () => {
  try {
    await api.post('/api/financial/transactions', newTxn.value)
    showAddModal.value = false
    newTxn.value = { account_id: accounts.value[0]?.account_id, type: 'expense', amount: 0, category: '', description: '', date: new Date().toISOString().split('T')[0] }
    loadData()
  } catch (err) { alert('Failed to create transaction') }
}

onMounted(loadData)
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.filters { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.filters select { padding: 0.5rem; border: 1px solid #ddd; border-radius: 8px; }
.transactions-list { display: grid; gap: 0.75rem; }
.transaction-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.txn-info { display: flex; flex-direction: column; gap: 0.25rem; }
.txn-category { font-weight: 600; color: #333; }
.txn-desc { color: #666; font-size: 0.9rem; }
.txn-date { color: #999; font-size: 0.8rem; }
.txn-amount { text-align: right; }
.txn-amount .income { color: #27ae60; font-weight: 700; font-size: 1.1rem; }
.txn-amount .expense { color: #e74c3c; font-weight: 700; font-size: 1.1rem; }
.fraud-badge { display: block; color: #e74c3c; font-size: 0.8rem; margin-top: 0.25rem; }
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