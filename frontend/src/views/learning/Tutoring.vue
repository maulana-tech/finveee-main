<template>
  <div class="page">
    <header class="header">
      <div class="header-left">
        <router-link to="/dashboard" class="back-link">&lt; BACK</router-link>
        <h1 class="title">/ AI_TUTORING</h1>
      </div>
    </header>

    <div class="content">
      <!-- Sessions List -->
      <div class="section-title">■ SESSIONS</div>
      
      <div v-if="sessions.length > 0" class="session-list">
        <div v-for="session in sessions" :key="session.session_id" class="session-card">
          <div class="session-head">
            <div class="session-topic">{{ session.topic || 'Learning Session' }}</div>
            <div class="session-status" :class="session.status">{{ session.status }}</div>
          </div>
          <div class="session-msgs">
            <div v-for="(msg, i) in session.messages" :key="i" class="msg-row" :class="msg.role">
              <div class="msg-role">{{ msg.role }}</div>
              <div class="msg-text">{{ msg.content }}</div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty">
        <div class="empty-icon">[S]</div>
        <div class="empty-text">No sessions yet</div>
      </div>

      <div class="divider"></div>

      <!-- New Session -->
      <div class="section-title">■ NEW_SESSION</div>
      
      <form @submit.prevent="startSession" class="new-form">
        <div class="form-group">
          <label>TOPIC</label>
          <input v-model="newSession.topic" type="text" placeholder="What do you want to learn?" required />
        </div>
        <button type="submit" class="btn-submit">START</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const sessions = ref([])
const newSession = ref({ topic: '', course_id: '' })

const loadSessions = async () => {
  try {
    const res = await api.get('/api/learning/tutoring')
    sessions.value = res.data.data || []
  } catch (err) { 
    console.error('Failed to load sessions:', err) 
  }
}

const startSession = async () => {
  try {
    await api.post('/api/learning/tutoring', newSession.value)
    newSession.value.topic = ''
    loadSessions()
  } catch (err) { 
    alert('Failed to start session') 
  }
}

onMounted(loadSessions)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

.page {
  min-height: 100vh;
  background: #fff;
  font-family: 'JetBrains Mono', monospace;
  color: #000;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 2px solid #000;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-link {
  color: #666;
  text-decoration: none;
  font-size: 11px;
}

.back-link:hover {
  color: #ff4500;
}

.title {
  font-size: 16px;
  font-weight: 700;
  color: #ff4500;
  letter-spacing: 2px;
  margin: 0;
}

.content {
  padding: 24px;
}

.section-title {
  font-size: 12px;
  font-weight: 700;
  color: #666;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.session-list {
  display: grid;
  gap: 16px;
  margin-bottom: 24px;
}

.session-card {
  padding: 20px;
  border: 2px solid #ccc;
  background: #fff;
}

.session-card:hover {
  border-color: #ff4500;
}

.session-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.session-topic {
  font-size: 14px;
  font-weight: 600;
}

.session-status {
  font-size: 10px;
  font-weight: 600;
  padding: 4px 10px;
}

.session-status.active {
  color: #1976d2;
  border: 1px solid #1976d2;
}

.session-status.completed {
  color: #27ae60;
  border: 1px solid #27ae60;
}

.session-msgs {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.msg-row {
  padding: 12px 16px;
}

.msg-row.user {
  background: #f0f4ff;
  margin-left: 24px;
}

.msg-row.assistant {
  background: #f5f5f5;
  margin-right: 24px;
}

.msg-role {
  font-size: 9px;
  color: #666;
  text-transform: capitalize;
  margin-bottom: 4px;
}

.msg-text {
  font-size: 12px;
}

.divider {
  height: 2px;
  background: #ccc;
  margin: 24px 0;
}

.new-form {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  font-size: 10px;
  font-weight: 600;
  color: #666;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 2px solid #ccc;
  font-family: inherit;
  font-size: 13px;
}

.form-group input:focus {
  outline: none;
  border-color: #ff4500;
}

.btn-submit {
  background: #000;
  border: 2px solid #000;
  color: #fff;
  padding: 12px 24px;
  font-family: inherit;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.btn-submit:hover {
  background: #ff4500;
  border-color: #ff4500;
}

.empty {
  padding: 60px;
  text-align: center;
  border: 2px solid #ccc;
  margin-bottom: 24px;
}

.empty-icon {
  font-size: 32px;
  color: #ccc;
  margin-bottom: 12px;
}

.empty-text {
  font-size: 14px;
  color: #666;
}
</style>