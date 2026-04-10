<template>
  <div class="page-container">
    <header class="page-header">
      <h1>Courses</h1>
      <button v-if="isTeacher" @click="showAddModal = true" class="btn-primary">+ Create Course</button>
    </header>
    
    <div class="filters">
      <select v-model="filterCategory">
        <option value="">All Categories</option>
        <option v-for="cat in categories" :value="cat">{{ cat }}</option>
      </select>
      <select v-model="filterDifficulty">
        <option value="">All Levels</option>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
    </div>
    
    <div class="courses-grid">
      <div v-for="course in filteredCourses" :key="course.course_id" class="course-card">
        <div class="course-header">
          <span class="badge">{{ course.category }}</span>
          <span class="difficulty">{{ course.difficulty }}</span>
        </div>
        <h3>{{ course.title }}</h3>
        <p>{{ course.description }}</p>
        <div class="course-meta">
          <span>⏱️ {{ course.duration_hours }} hours</span>
          <span>📚 {{ course.modules?.length || 0 }} lessons</span>
        </div>
        <button v-if="!isEnrolled(course.course_id)" @click="enroll(course.course_id)" class="btn-enroll">
          Enroll
        </button>
        <span v-else class="enrolled-badge">✓ Enrolled</span>
      </div>
      
      <div v-if="filteredCourses.length === 0" class="empty-state">
        <p>No courses found.</p>
      </div>
    </div>
    
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <h2>Create Course</h2>
        <form @submit.prevent="createCourse">
          <div class="form-group">
            <label>Title</label>
            <input v-model="newCourse.title" type="text" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newCourse.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Category</label>
            <select v-model="newCourse.category">
              <option v-for="cat in categories" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Difficulty</label>
            <select v-model="newCourse.difficulty">
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
          <div class="form-group">
            <label>Duration (hours)</label>
            <input v-model.number="newCourse.duration_hours" type="number" step="0.5" />
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
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const courses = ref([])
const enrollments = ref([])
const filterCategory = ref('')
const filterDifficulty = ref('')
const showAddModal = ref(false)
const isTeacher = ref(false)

const categories = ['Programming', 'Data Science', 'Business', 'Language', 'Science', 'Math']
const newCourse = ref({ title: '', description: '', category: 'Programming', difficulty: 'beginner', duration_hours: 1, modules: [] })

const filteredCourses = computed(() => {
  return courses.value.filter(c => {
    if (filterCategory.value && c.category !== filterCategory.value) return false
    if (filterDifficulty.value && c.difficulty !== filterDifficulty.value) return false
    return true
  })
})

const isEnrolled = (courseId) => enrollments.value.some(e => e.course_id === courseId)

const loadData = async () => {
  try {
    const [coursesRes, enrRes] = await Promise.all([api.get('/api/learning/courses'), api.get('/api/learning/enrollments')])
    courses.value = coursesRes.data.data || []
    enrollments.value = enrRes.data.data || []
  } catch (err) { console.error('Failed to load data:', err) }
}

const enroll = async (courseId) => {
  try {
    await api.post('/api/learning/enrollments', { course_id: courseId })
    loadData()
  } catch (err) { alert('Failed to enroll') }
}

const createCourse = async () => {
  try {
    await api.post('/api/learning/courses', newCourse.value)
    showAddModal.value = false
    loadData()
  } catch (err) { alert('Failed to create course') }
}

onMounted(loadData)
</script>

<style scoped>
.page-container { padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.filters { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.filters select { padding: 0.5rem; border: 1px solid #ddd; border-radius: 8px; }
.courses-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
.course-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; flex-direction: column; }
.course-header { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; }
.badge { background: #e8eaf6; color: #667eea; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; }
.difficulty { background: #f5f5f5; color: #666; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; text-transform: capitalize; }
.course-card h3 { margin: 0 0 0.5rem; color: #333; }
.course-card p { flex: 1; color: #666; font-size: 0.9rem; margin-bottom: 1rem; }
.course-meta { display: flex; gap: 1rem; color: #999; font-size: 0.85rem; margin-bottom: 1rem; }
.btn-enroll { background: #667eea; color: white; border: none; padding: 0.75rem; border-radius: 8px; cursor: pointer; }
.enrolled-badge { color: #27ae60; font-weight: 600; text-align: center; }
.empty-state { text-align: center; padding: 2rem; color: #666; }
.btn-primary { background: #667eea; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; }
.btn-secondary { background: #ddd; color: #333; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 100%; max-width: 500px; max-height: 90vh; overflow-y: auto; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; }
.form-actions { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1.5rem; }
</style>