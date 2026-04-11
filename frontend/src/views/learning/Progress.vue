<template>
  <div class="page">
    <header class="header">
      <div class="header-left">
        <router-link to="/dashboard" class="back-link">&lt; BACK</router-link>
        <h1 class="title">/ PROGRESS</h1>
      </div>
    </header>

    <div class="content">
      <!-- Stats -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-label">TOTAL_COURSES</div>
          <div class="stat-val">{{ enrollments.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">COMPLETED</div>
          <div class="stat-val done">{{ completedCount }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">IN_PROGRESS</div>
          <div class="stat-val prog">{{ inProgressCount }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">AVG_PROGRESS</div>
          <div class="stat-val">{{ averageProgress }}%</div>
        </div>
      </div>

      <div class="divider"></div>

      <!-- Recommendations -->
      <div v-if="recommendations.length" class="section">
        <div class="section-title">■ RECOMMENDED</div>
        <div class="rec-list">
          <div v-for="rec in recommendations" :key="rec.course.course_id" class="rec-card">
            <div class="rec-title">{{ rec.course.title }}</div>
            <div class="rec-reason">{{ rec.reason }}</div>
            <button @click="enroll(rec.course.course_id)" class="btn-enroll">ENROLL</button>
          </div>
        </div>
      </div>

      <div v-if="enrollments.length === 0" class="empty">
        <div class="empty-icon">[R]</div>
        <div class="empty-text">No learning progress yet</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const enrollments = ref([])
const recommendations = ref([])

const completedCount = computed(() => enrollments.value.filter(e => e.status === 'completed').length)
const inProgressCount = computed(() => enrollments.value.filter(e => e.status === 'in_progress').length)
const averageProgress = computed(() => {
  if (!enrollments.value.length) return 0
  return (enrollments.value.reduce((sum, e) => sum + e.progress_percent, 0) / enrollments.value.length).toFixed(0)
})

const loadData = async () => {
  try {
    const [enrRes, recRes] = await Promise.all([
      api.get('/api/learning/enrollments'),
      api.get('/api/learning/recommendations?skill_level=beginner')
    ])
    enrollments.value = enrRes.data.data || []
    recommendations.value = recRes.data.data || []
  } catch (err) { 
    console.error('Failed to load data:', err) 
  }
}

const enroll = async (courseId) => {
  try {
    await api.post('/api/learning/enrollments', { course_id: courseId })
    loadData()
  } catch (err) { 
    alert('Failed to enroll') 
  }
}

onMounted(loadData)
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

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  padding: 20px;
  border: 2px solid #ccc;
  text-align: center;
}

.stat-label {
  font-size: 10px;
  font-weight: 600;
  color: #666;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.stat-val {
  font-size: 28px;
  font-weight: 700;
}

.stat-val.done {
  color: #27ae60;
}

.stat-val.prog {
  color: #f39c12;
}

.divider {
  height: 2px;
  background: #ccc;
  margin: 24px 0;
}

.section-title {
  font-size: 12px;
  font-weight: 700;
  color: #666;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.rec-list {
  display: grid;
  gap: 12px;
}

.rec-card {
  padding: 16px 20px;
  border: 2px solid #ccc;
  background: #fff;
  display: flex;
  align-items: center;
  gap: 16px;
}

.rec-card:hover {
  border-color: #ff4500;
}

.rec-title {
  flex: 1;
  font-size: 13px;
  font-weight: 600;
}

.rec-reason {
  font-size: 11px;
  color: #666;
}

.btn-enroll {
  background: #000;
  border: 2px solid #000;
  color: #fff;
  padding: 8px 16px;
  font-family: inherit;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
}

.btn-enroll:hover {
  background: #ff4500;
  border-color: #ff4500;
}

.empty {
  padding: 60px;
  text-align: center;
  border: 2px solid #ccc;
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

@media (max-width: 900px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>