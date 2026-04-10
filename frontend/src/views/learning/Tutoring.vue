<template>
  <div class="page-container">
    <h1>AI Tutoring</h1>
    
    <div class="sessions-list">
      <div v-for="session in sessions" :key="session.session_id" class="session-card">
        <div class="session-header">
          <h3>{{ session.topic || 'Learning Session' }}</h3>
          <span class="status" :class="session.status">{{ session.status }}</span>
        </div>
        <div class="messages">
          <div v-for="(msg, i) in session.messages" :key="i" class="message" :class="msg.role">
            <span class="role">{{ msg.role }}</span>
            <p>{{ msg.content }}</p>
          </div>
        </div>
      </div>
      
      <div v-if="sessions.length === 0" class="empty-state">
        <p>No tutoring sessions yet. Start a new session!</p>
      </div>
    </div>
    
    <div class="new-session">
      <h2>Start New Session</h2>
      <form @submit.prevent="startSession">
        <div class="form-group">
          <label>Topic</label>
          <input v-model="newSession.topic" type="text" placeholder="What do you want to learn?" required />
        </div>
        <button type="submit" class="btn-primary">Start Tutoring</button>
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
  } catch (err) { console.error('Failed to load sessions:', err) }
}

const startSession = async () => {
  try {
    await api.post('/api/learning/tutoring', newSession.value)
    newSession.value.topic = ''
    loadSessions()
  } catch (err) { alert('Failed to start session') }
}

onMounted(loadSessions)
</script>

<style scoped>
.page-container { padding: 2rem; }
h1 { margin-bottom: 2rem; }
.sessions-list { display: grid; gap: 1.5rem; margin-bottom: 2rem; }
.session-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.session-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.session-header h3 { margin: 0; color: #333; }
.status { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; }
.status.active { background: #e3f2fd; color: #1976d2; }
.status.completed { background: #e8f5e9; color: #388e3c; }
.messages { display: flex; flex-direction: column; gap: 1rem; }
.message { padding: 1rem; border-radius: 8px; }
.message.user { background: #f0f4ff; margin-left: 2rem; }
.message.assistant { background: #f5f5f5; margin-right: 2rem; }
.message .role { font-size: 0.8rem; color: #666; text-transform: capitalize; }
.message p { margin: 0.25rem 0 0; }
.new-session { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.new-session h2 { margin: 0 0 1rem; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.form-group input { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; }
.btn-primary { background: #667eea; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; }
.empty-state { text-align: center; padding: 2rem; color: #666; }
</style>