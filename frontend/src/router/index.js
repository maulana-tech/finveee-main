import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Process from '../views/MainView.vue'
import SimulationView from '../views/SimulationView.vue'
import SimulationRunView from '../views/SimulationRunView.vue'
import ReportView from '../views/ReportView.vue'
import InteractionView from '../views/InteractionView.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import FinancialAccounts from '../views/financial/Accounts.vue'
import FinancialTransactions from '../views/financial/Transactions.vue'
import FinancialBudgets from '../views/financial/Budgets.vue'
import FinancialAnalytics from '../views/financial/Analytics.vue'
import FinancialFraud from '../views/financial/FraudDetection.vue'
import LearningCourses from '../views/learning/Courses.vue'
import LearningEnrollments from '../views/learning/Enrollments.vue'
import LearningTutoring from '../views/learning/Tutoring.vue'
import LearningProgress from '../views/learning/Progress.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/process/:projectId',
    name: 'Process',
    component: Process,
    props: true
  },
  {
    path: '/simulation/:simulationId',
    name: 'Simulation',
    component: SimulationView,
    props: true
  },
  {
    path: '/simulation/:simulationId/start',
    name: 'SimulationRun',
    component: SimulationRunView,
    props: true
  },
  {
    path: '/report/:reportId',
    name: 'Report',
    component: ReportView,
    props: true
  },
  {
    path: '/interaction/:reportId',
    name: 'Interaction',
    component: InteractionView,
    props: true
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  // Financial routes
  {
    path: '/financial/accounts',
    name: 'FinancialAccounts',
    component: FinancialAccounts
  },
  {
    path: '/financial/transactions',
    name: 'FinancialTransactions',
    component: FinancialTransactions
  },
  {
    path: '/financial/budgets',
    name: 'FinancialBudgets',
    component: FinancialBudgets
  },
  {
    path: '/financial/analytics',
    name: 'FinancialAnalytics',
    component: FinancialAnalytics
  },
  {
    path: '/financial/fraud',
    name: 'FinancialFraud',
    component: FinancialFraud
  },
  // Learning routes
  {
    path: '/learning/courses',
    name: 'LearningCourses',
    component: LearningCourses
  },
  {
    path: '/learning/enrollments',
    name: 'LearningEnrollments',
    component: LearningEnrollments
  },
  {
    path: '/learning/tutoring',
    name: 'LearningTutoring',
    component: LearningTutoring
  },
  {
    path: '/learning/progress',
    name: 'LearningProgress',
    component: LearningProgress
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router