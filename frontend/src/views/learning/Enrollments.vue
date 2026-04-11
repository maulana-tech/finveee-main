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
        <span class="nav-link active">ENROLLMENTS</span>
        <button @click="logout" class="btn-logout">[X]</button>
      </nav>
    </header>

    <div class="body">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-label">■ LEARNING</div>
        
        <router-link to="/learning/courses" class="nav-item">
          <span class="nav-icon">[C]</span>
          <span class="nav-text">Courses</span>
        </router-link>
        <router-link to="/learning/enrollments" class="nav-item" :class="{ active: true }">
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
          <h1 class="tab-title">/ ENROLLMENTS</h1>
          <span class="tab-time">{{ currentTime }}</span>
        </div>

        <!-- Stats -->
        <div class="stats-row">
          <div class="stat-card large">
            <div class="stat-name">TOTAL</div>
            <div class="stat-val">{{ enrollments.length }}</div>
          </div>
          <div class="stat-card large">
            <div class="stat-name">COMPLETED</div>
            <div class="stat-val done">{{ completedCount }}</div>
          </div>
          <div class="stat-card large">
            <div class="stat-name">IN_PROGRESS</div>
            <div class="stat-val prog">{{ inProgressCount }}</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="section-label">■ ENROLLMENTS_LIST</div>

        <div class="card-grid">
          <div v-for="enrollment in enrollments" :key="enrollment.enrollment_id" class="card big">
            <div class="card-left">
              <div class="card-icon-lg">[E]</div>
            </div>
            <div class="card-mid">
              <div class="card-name-lg">{{ enrollment.course_title || 'Course' }}</div>
              <div class="card-type-lg">{{ enrollment.status }}</div>
            </div>
            <div class="card-right">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: enrollment.progress_percent + '%' }"></div>
              </div>
              <div class="progress-text">{{ enrollment.progress_percent.toFixed(0) }}% COMPLETE</div>
            </div>
          </div>

          <div v-if="enrollments.length === 0" class="empty-card">
            <div class="empty-icon">[E]</div>
            <div class="empty-text">No enrollments yet</div>
            <router-link to="/learning/courses" class="btn-primary">BROWSE_COURSES</router-link>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const enrollments = ref([])
const currentTime = ref('')

const completedCount = computed(() => enrollments.value.filter(e => e.status === 'completed').length)
const inProgressCount = computed(() => enrollments.value.filter(e => e.status === 'in_progress').length)

const updateTime = () => { currentTime.value = new Date().toISOString().slice(0, 19).replace('T', ' ') }
let timeInterval
onMounted(() => { updateTime(); timeInterval = setInterval(updateTime, 1000) })
onUnmounted(() => clearInterval(timeInterval))

const switchTab = (tab) => router.push('/dashboard?tab=' + tab)
const logout = () => { localStorage.removeItem('token'); localStorage.removeItem('user'); router.push('/login') }

const loadEnrollments = async () => {
  try {
    const res = await api.get('/api/learning/enrollments')
    enrollments.value = res.data.data || []
  } catch (err) { console.error('Failed to load enrollments:', err) }
}

onMounted(loadEnrollments)
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

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card.large { padding: 28px; border: 2px solid #ccc; background: #fff; }
.stat-name { font-size: 11px; font-weight: 600; color: #666; letter-spacing: 1px; margin-bottom: 12px; }
.stat-val { font-size: 32px; font-weight: 700; }
.stat-val.done { color: #27ae60; }
.stat-val.prog { color: #f39c12; }

.divider { height: 2px; background: #ccc; margin: 24px 0; }
.section-label { font-size: 12px; font-weight: 700; color: #666; letter-spacing: 1px; margin-bottom: 16px; }

.card-grid { display: grid; gap: 16px; }
.card.big { display: flex; align-items: center; padding: 24px; border: 2px solid #ccc; background: #fff; transition: all 0.15s; }
.card.big:hover { border-color: #ff4500; }
.card-icon-lg { font-size: 32px; font-weight: 700; color: #ff4500; margin-right: 20px; }
.card-mid { flex: 1; }
.card-name-lg { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
.card-type-lg { font-size: 12px; color: #666; text-transform: capitalize; }
.card-right { text-align: right; }
.progress-bar { height: 14px; background: #eee; border: 1px solid #ccc; width: 120px; }
.progress-fill { height: 100%; background: #ff4500; transition: width 0.3s; }
.progress-text { font-size: 11px; color: #666; margin-top: 6px; }

.empty-card { padding: 60px; text-align: center; border: 2px solid #ccc; }
.empty-icon { font-size: 48px; color: #ccc; margin-bottom: 16px; }
.empty-text { font-size: 16px; color: #666; margin-bottom: 20px; }
.btn-primary { background: #000; border: 2px solid #000; color: #fff; padding: 12px 24px; font-family: inherit; font-size: 12px; font-weight: 600; text-decoration: none; }
.btn-primary:hover { background: #ff4500; border-color: #ff4500; }

@media (max-width: 768px) { .sidebar { display: none; } .stats-row { grid-template-columns: 1fr; } }
</style>