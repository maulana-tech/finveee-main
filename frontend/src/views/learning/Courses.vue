<template>
  <div class="layout">
    <!-- Header -->
    <header class="header">
      <div class="brand">
        <span class="brand-square">■</span>
        <span class="brand-name">FINVEE</span>
      </div>
      <nav class="header-nav">
        <router-link to="/" class="nav-link">HOME</router-link>
        <span class="nav-sep">|</span>
        <router-link to="/dashboard" class="nav-link">DASHBOARD</router-link>
        <span class="nav-sep">|</span>
        <span class="nav-link active">COURSES</span>
        <button @click="logout" class="btn-logout">[X]</button>
      </nav>
    </header>

    <div class="body">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-label">■ LEARNING</div>
        
        <router-link to="/learning/courses" class="nav-item" :class="{ active: true }">
          <span class="nav-icon">[C]</span>
          <span class="nav-text">Courses</span>
        </router-link>
        <router-link to="/learning/enrollments" class="nav-item">
          <span class="nav-icon">[E]</span>
          <span class="nav-text">Enrollments</span>
        </router-link>
        <router-link to="/learning/tutoring" class="nav-item">
          <span class="nav-icon">[S]</span>
          <span class="nav-text">AI Tutoring</span>
        </router-link>
        <router-link to="/learning/progress" class="nav-item">
          <span class="nav-icon">[R]</span>
          <span class="nav-text">Progress</span>
        </router-link>

        <div class="sidebar-divider"></div>

        <div class="sidebar-label">■ MODULES</div>
        
        <button @click="switchTab('financial')" class="nav-item">
          <span class="nav-icon">[$]</span>
          <span class="nav-text">Financial</span>
        </button>
        <button @click="switchTab('learning')" class="nav-item">
          <span class="nav-icon">[#]</span>
          <span class="nav-text">Learning</span>
        </button>
        <button @click="switchTab('simulation')" class="nav-item">
          <span class="nav-icon">[S]</span>
          <span class="nav-text">Simulation</span>
        </button>
      </aside>

      <!-- Main Content -->
      <main class="main">
        <div class="tab-header">
          <h1 class="tab-title">/ COURSES</h1>
          <span class="tab-time">{{ currentTime }}</span>
        </div>

        <!-- Filters -->
        <div class="filters-row">
          <select v-model="filterCategory" class="filter-select">
            <option value="">All Categories</option>
            <option v-for="cat in categories" :value="cat">{{ cat }}</option>
          </select>
          <select v-model="filterDifficulty" class="filter-select">
            <option value="">All Levels</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <!-- Stats -->
        <div class="stats-row">
          <div class="stat-card large">
            <div class="stat-name">TOTAL_COURSES</div>
            <div class="stat-val">{{ filteredCourses.length }}</div>
          </div>
          <div class="stat-card large">
            <div class="stat-name">ENROLLED</div>
            <div class="stat-val">{{ enrollments.length }}</div>
          </div>
          <div class="stat-card large">
            <div class="stat-name">COMPLETED</div>
            <div class="stat-val done">{{ completedCount }}</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section-label">■ COURSES_LIST</div>

        <div class="card-grid">
          <div v-for="course in filteredCourses" :key="course.course_id" class="card big">
            <div class="card-left">
              <div class="card-icon-lg">[C]</div>
            </div>
            <div class="card-mid">
              <div class="card-name-lg">{{ course.title }}</div>
              <div class="card-type-lg">{{ course.description }}</div>
              <div class="card-meta">
                <span>{{ course.duration_hours }} hours</span>
                <span>{{ course.modules?.length || 0 }} lessons</span>
                <span class="level">{{ course.difficulty }}</span>
              </div>
            </div>
            <div class="card-right">
              <button v-if="!isEnrolled(course.course_id)" @click="enroll(course.course_id)" class="btn-enroll">ENROLL</button>
              <div v-else class="enrolled-tag">ENROLLED</div>
            </div>
          </div>

          <div v-if="filteredCourses.length === 0" class="empty-card">
            <div class="empty-icon">[C]</div>
            <div class="empty-text">No courses found</div>
          </div>
        </div>

        <button v-if="isTeacher" @click="showAddModal = true" class="btn-add-float">+</button>
      </main>
    </div>

    <!-- Create Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2>NEW_COURSE</h2>
          <button @click="showAddModal = false" class="modal-close">[X]</button>
        </div>
        <form @submit.prevent="createCourse" class="form">
          <div class="form-group">
            <label>TITLE</label>
            <input v-model="newCourse.title" type="text" required />
          </div>
          <div class="form-group">
            <label>DESCRIPTION</label>
            <textarea v-model="newCourse.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>CATEGORY</label>
            <select v-model="newCourse.category">
              <option v-for="cat in categories" :value="cat">{{ cat }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>DIFFICULTY</label>
            <select v-model="newCourse.difficulty">
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
          <div class="form-group">
            <label>DURATION_HOURS</label>
            <input v-model.number="newCourse.duration_hours" type="number" step="0.5" />
          </div>
          <div class="form-actions">
            <button type="button" @click="showAddModal = false" class="btn-cancel">CANCEL</button>
            <button type="submit" class="btn-submit">CREATE</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()

const courses = ref([])
const enrollments = ref([])
const filterCategory = ref('')
const filterDifficulty = ref('')
const showAddModal = ref(false)
const isTeacher = ref(false)
const currentTime = ref('')

const categories = ['Programming', 'Data Science', 'Business', 'Language', 'Science', 'Math']
const newCourse = ref({ title: '', description: '', category: 'Programming', difficulty: 'beginner', duration_hours: 1, modules: [] })

const filteredCourses = computed(() => {
  return courses.value.filter(c => {
    if (filterCategory.value && c.category !== filterCategory.value) return false
    if (filterDifficulty.value && c.difficulty !== filterDifficulty.value) return false
    return true
  })
})

const completedCount = computed(() => enrollments.value.filter(e => e.status === 'completed').length)
const isEnrolled = (courseId) => enrollments.value.some(e => e.course_id === courseId)

const updateTime = () => { currentTime.value = new Date().toISOString().slice(0, 19).replace('T', ' ') }
let timeInterval
onMounted(() => { updateTime(); timeInterval = setInterval(updateTime, 1000) })
onUnmounted(() => clearInterval(timeInterval))

const switchTab = (tab) => router.push('/dashboard?tab=' + tab)
const logout = () => { localStorage.removeItem('token'); localStorage.removeItem('user'); router.push('/login') }

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
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

.layout { min-height: 100vh; background: #fff; font-family: 'JetBrains Mono', monospace; color: #000; }
.header { display: flex; justify-content: space-between; align-items: center; padding: 12px 24px; background: #000; border-bottom: 2px solid #000; }
.brand { display: flex; align-items: center; gap: 6px; }
.brand-square { color: #ff4500; font-size: 10px; }
.brand-name { color: #fff; font-size: 14px; font-weight: 700; letter-spacing: 2px; }
.header-nav { display: flex; align-items: center; gap: 12px; }
.nav-link { color: #888; text-decoration: none; font-size: 12px; }
.nav-link:hover { color: #fff; }
.nav-link.active { color: #ff4500; }
.nav-sep { color: #444; }
.btn-logout { background: transparent; border: 1px solid #ff4500; color: #ff4500; padding: 4px 10px; font-family: inherit; font-size: 11px; cursor: pointer; }
.btn-logout:hover { background: #ff4500; color: #000; }

.body { display: flex; min-height: calc(100vh - 52px); }
.sidebar { width: 200px; background: #f8f8f8; border-right: 2px solid #ccc; padding: 20px 0; flex-shrink: 0; }
.sidebar-label { font-size: 10px; font-weight: 700; color: #666; padding: 0 16px; margin-bottom: 12px; letter-spacing: 1px; }
.sidebar-divider { height: 2px; background: #ddd; margin: 16px; }
.nav-item { display: flex; align-items: center; gap: 10px; width: calc(100% - 32px); margin: 0 16px; padding: 10px 12px; background: transparent; border: none; border-left: 2px solid transparent; color: #333; font-family: inherit; font-size: 12px; text-decoration: none; cursor: pointer; transition: all 0.15s; }
.nav-item:hover { background: #eee; border-left-color: #aaa; }
.nav-item.active { background: #fff; border-left-color: #ff4500; color: #ff4500; }
.nav-icon { font-size: 11px; color: #888; width: 20px; }
.nav-item:hover .nav-icon, .nav-item.active .nav-icon { color: #ff4500; }

.main { flex: 1; padding: 24px; background: #fff; }
.tab-header { display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 16px; border-bottom: 2px solid #000; margin-bottom: 24px; }
.tab-title { font-size: 20px; font-weight: 700; color: #ff4500; letter-spacing: 2px; margin: 0; }
.tab-time { font-size: 11px; color: #888; }

.filters-row { display: flex; gap: 12px; margin-bottom: 16px; }
.filter-select { padding: 12px 16px; border: 2px solid #ccc; font-family: inherit; font-size: 12px; }

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card.large { padding: 28px; border: 2px solid #ccc; background: #fff; }
.stat-name { font-size: 11px; font-weight: 600; color: #666; letter-spacing: 1px; margin-bottom: 12px; }
.stat-val { font-size: 32px; font-weight: 700; }
.stat-val.done { color: #27ae60; }

.divider { height: 2px; background: #ccc; margin: 24px 0; }
.section-label { font-size: 12px; font-weight: 700; color: #666; letter-spacing: 1px; margin-bottom: 16px; }

.card-grid { display: grid; gap: 16px; }
.card.big { display: flex; align-items: center; padding: 24px; border: 2px solid #ccc; background: #fff; transition: all 0.15s; }
.card.big:hover { border-color: #ff4500; }
.card-icon-lg { font-size: 32px; font-weight: 700; color: #ff4500; margin-right: 20px; }
.card-mid { flex: 1; }
.card-name-lg { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
.card-type-lg { font-size: 12px; color: #666; margin-bottom: 8px; }
.card-meta { display: flex; gap: 16px; font-size: 11px; color: #999; }
.card-meta .level { text-transform: capitalize; }
.card-right { text-align: right; }
.btn-enroll { background: #000; border: 2px solid #000; color: #fff; padding: 10px 20px; font-family: inherit; font-size: 11px; font-weight: 600; cursor: pointer; }
.btn-enroll:hover { background: #ff4500; border-color: #ff4500; }
.enrolled-tag { font-size: 11px; color: #27ae60; font-weight: 600; padding: 10px 20px; border: 2px solid #27ae60; }

.empty-card { padding: 60px; text-align: center; border: 2px solid #ccc; }
.empty-icon { font-size: 48px; color: #ccc; margin-bottom: 16px; }
.empty-text { font-size: 16px; color: #666; }

.btn-add-float { position: fixed; bottom: 32px; right: 32px; width: 56px; height: 56px; background: #ff4500; border: 2px solid #ff4500; color: #fff; font-size: 28px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(255, 69, 0, 0.4); }
.btn-add-float:hover { background: #000; border-color: #000; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; border: 2px solid #000; width: 100%; max-width: 500px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 2px solid #ccc; }
.modal-header h2 { font-size: 14px; margin: 0; letter-spacing: 1px; }
.modal-close { background: none; border: none; color: #666; font-family: inherit; font-size: 14px; cursor: pointer; }
.form { padding: 20px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 10px; font-weight: 600; color: #666; margin-bottom: 8px; letter-spacing: 1px; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 14px; border: 2px solid #ccc; font-family: inherit; font-size: 14px; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #ff4500; }
.form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 24px; }
.btn-cancel { background: #fff; border: 2px solid #ccc; color: #666; padding: 12px 24px; font-family: inherit; font-size: 12px; cursor: pointer; }
.btn-cancel:hover { border-color: #333; }
.btn-submit { background: #000; border: 2px solid #000; color: #fff; padding: 12px 24px; font-family: inherit; font-size: 12px; font-weight: 600; cursor: pointer; }
.btn-submit:hover { background: #ff4500; border-color: #ff4500; }

@media (max-width: 768px) { .sidebar { display: none; } .stats-row { grid-template-columns: 1fr; } }
</style>