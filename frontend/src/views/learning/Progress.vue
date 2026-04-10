<template>
  <div class="page-container">
    <h1>Learning Progress</h1>
    
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total Courses</h3>
        <p>{{ enrollments.length }}</p>
      </div>
      <div class="stat-card">
        <h3>Completed</h3>
        <p class="completed">{{ completedCount }}</p>
      </div>
      <div class="stat-card">
        <h3>In Progress</h3>
        <p class="in-progress">{{ inProgressCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Avg Progress</h3>
        <p>{{ averageProgress }}%</p>
      </div>
    </div>
    
    <div class="recommendations" v-if="recommendations.length">
      <h2>Recommended for You</h2>
      <div class="rec-list">
        <div v-for="rec in recommendations" :key="rec.course.course_id" class="rec-card">
          <h3>{{ rec.course.title }}</h3>
          <p>{{ rec.reason }}</p>
          <button @click="enroll(rec.course.course_id)" class="btn-enroll">Enroll Now</button>
        </div>
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
  } catch (err) { console.error('Failed to load data:', err) }
}

const enroll = async (courseId) => {
  try {
    await api.post('/api/learning/enrollments', { course_id: courseId })
    loadData()
  } catch (err) { alert('Failed to enroll') }
}

onMounted(loadData)
</script>

<style scoped>
.page-container { padding: 2rem; }
h1 { margin-bottom: 2rem; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.stat-card h3 { margin: 0 0 0.5rem; color: #666; font-size: 0.9rem; }
.stat-card p { margin: 0; font-size: 2rem; font-weight: 700; color: #333; }
.stat-card p.completed { color: #27ae60; }
.stat-card p.in-progress { color: #f39c12; }
.recommendations { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.recommendations h2 { margin: 0 0 1rem; }
.rec-list { display: grid; gap: 1rem; }
.rec-card { padding: 1rem; border: 1px solid #eee; border-radius: 8px; }
.rec-card h3 { margin: 0 0 0.5rem; color: #333; }
.rec-card p { margin: 0 0 1rem; color: #666; font-size: 0.9rem; }
.btn-enroll { background: #667eea; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; }
</style>