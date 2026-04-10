<template>
  <div class="page-container">
    <header class="page-header">
      <h1>Accounts</h1>
      <button @click="showAddModal = true" class="btn-primary">+ Add Account</button>
    </header>
    
    <div class="accounts-list">
      <div v-for="account in accounts" :key="account.account_id" class="account-card">
        <div class="account-icon">{{ getAccountIcon(account.account_type) }}</div>
        <div class="account-info">
          <h3>{{ account.name }}</h3>
          <p>{{ account.account_type }}</p>
        </div>
        <div class="account-balance">
          <span class="currency">{{ account.currency }}</span>
          <span class="amount">{{ account.balance.toLocaleString() }}</span>
        </div>
      </div>
      
      <div v-if="accounts.length === 0" class="empty-state">
        <p>No accounts yet. Add your first account to get started!</p>
      </div>
    </div>
    
    <!-- Add Account Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <h2>Add New Account</h2>
        <form @submit.prevent="createAccount">
          <div class="form-group">
            <label>Account Name</label>
            <input v-model="newAccount.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Account Type</label>
            <select v-model="newAccount.account_type" required>
              <option value="checking">Checking</option>
              <option value="savings">Savings</option>
              <option value="credit">Credit Card</option>
              <option value="investment">Investment</option>
            </select>
          </div>
          <div class="form-group">
            <label>Initial Balance</label>
            <input v-model.number="newAccount.initial_balance" type="number" step="0.01" />
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

const accounts = ref([])
const showAddModal = ref(false)
const newAccount = ref({
  name: '',
  account_type: 'checking',
  initial_balance: 0
})

const getAccountIcon = (type) => {
  const icons = { checking: '🏦', savings: '💰', credit: '💳', investment: '📈' }
  return icons[type] || '🏦'
}

const loadAccounts = async () => {
  try {
    const res = await api.get('/api/financial/accounts')
    accounts.value = res.data.data || []
  } catch (err) {
    console.error('Failed to load accounts:', err)
  }
}

const createAccount = async () => {
  try {
    await api.post('/api/financial/accounts', newAccount.value)
    showAddModal.value = false
    newAccount.value = { name: '', account_type: 'checking', initial_balance: 0 }
    loadAccounts()
  } catch (err) {
    alert('Failed to create account')
  }
}

onMounted(loadAccounts)
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.accounts-list { display: grid; gap: 1rem; }
.account-card { display: flex; align-items: center; gap: 1rem; background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.account-icon { font-size: 2rem; }
.account-info { flex: 1; }
.account-info h3 { margin: 0; color: #333; }
.account-info p { margin: 0.25rem 0 0; color: #666; font-size: 0.9rem; text-transform: capitalize; }
.account-balance { text-align: right; }
.account-balance .currency { color: #666; font-size: 0.9rem; }
.account-balance .amount { font-size: 1.5rem; font-weight: 700; color: #333; margin-left: 0.25rem; }
.empty-state { text-align: center; padding: 3rem; color: #666; }
.btn-primary { background: #667eea; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; }
.btn-secondary { background: #ddd; color: #333; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 100%; max-width: 400px; }
.modal h2 { margin-top: 0; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.form-group input, .form-group select { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; }
.form-actions { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>