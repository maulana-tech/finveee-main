<template>
  <div class="page-container">
    <h1>My Learning</h1>
    
    <div class="enrollments-list">
      <div v-for="enrollment in enrollments" :key="enrollment.enrollment_id" class="enrollment-card">
        <div class="enrollment-info">
          <h3>{{ enrollment.course_title || 'Course' }}</h3>
          <span class="status" :class="enrollment.status">{{ enrollment.status }}</span>
        </div>
        <div class="progress-section">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: enrollment.progress_percent + '%' }"></div>
          </div>
          <span class="progress-text">{{ enrollment.progress_percent.toFixed(0) }}% Complete</span>
        </div>
      </div>
      
      <div v-if="enrollments.length === 0" class="empty-state">
        <p>No enrollments yet. <router-link to="/learning/courses">Browse courses</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const enrollments = ref([])

const loadEnrollments = async () => {
  try {
    const res = await api.get('/api/learning/enrollments')
    enrollments.value = res.data.data || []
  } catch (err) { console.error('Failed to load enrollments:', err) }
}

onMounted(loadEnrollments)
</script>

<style scoped>
.page-container { padding: 2rem; }
h1 { margin-bottom: 2rem; }
.enrollments-list { display: grid; gap: 1rem; }
.enrollment-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.enrollment-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.enrollment-info h3 { margin: 0; color: #333; }
.status { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; text-transform: capitalize; }
.status.enrolled { background: #e3f2fd; color: #1976d2; }
.status.in_progress { background: #fff3e0; color: #f57c00; }
.status.completed { background: #e8f5e9; color: #388e3c; }
.progress-bar { height: 8px; background: #eee; border-radius: 4px; overflow: hidden; margin-bottom: 0.5rem; }
.progress-fill { height: 100%; background: #667eea; transition: width 0.3s; }
.progress-text { font-size: 0.9rem; color: #666; }
.empty-state { text-align: center; padding: 2rem; color: #666; }
.empty-state a { color: #667eea; }
</style>