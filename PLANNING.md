# Finvee Refactoring Plan

## Project Overview

- **Name**: Finvee
- **Purpose**: A unified platform combining FinTech AI and EdTech AI
- **Focus**: 
  - FinTech AI: Fraud detection, financial management, tracking, analytics
  - EdTech AI: Personalized learning, tutoring, education management

## Current State

The existing codebase is "MiroFish" - a social simulation engine using OASIS (camel-ai) for multi-agent simulation. It includes:
- Flask backend with graph-based entity management (Zep)
- Vue 3 frontend with multi-step workflow
- LLM-powered simulation and report generation

## Refactoring Strategy

### Phase 1: Architecture Redesign

**New Modules:**
1. **Financial Module** (FinTech)
   - Transaction management
   - Budget tracking
   - Expense analytics
   - Fraud detection (AI-powered)
   - Financial reports

2. **Learning Module** (EdTech)
   - Course management
   - Student profiles
   - AI tutoring
   - Progress tracking
   - Personalized recommendations

3. **Core Module** (Shared)
   - User authentication
   - Dashboard
   - Settings
   - AI integration layer

### Phase 2: Backend Restructuring

```
backend/app/
├── core/              # Core services
│   ├── auth.py        # Authentication
│   ├── user.py        # User management
│   └── ai_client.py   # LLM integration
├── financial/         # FinTech services
│   ├── models/        # Financial models
│   ├── services/      # Business logic
│   └── api/           # API routes
├── learning/          # EdTech services
│   ├── models/        # Learning models
│   ├── services/      # Business logic
│   └── api/           # API routes
└── utils/             # Shared utilities
```

### Phase 3: Frontend Redesign

```
frontend/src/
├── views/
│   ├── Dashboard.vue
│   ├── Financial/
│   │   ├── Transactions.vue
│   │   ├── Budget.vue
│   │   ├── Analytics.vue
│   │   └── FraudDetection.vue
│   ├── Learning/
│   │   ├── Courses.vue
│   │   ├── Students.vue
│   │   ├── Tutoring.vue
│   │   └── Progress.vue
│   └── Auth/
│       ├── Login.vue
│       └── Register.vue
├── components/
│   ├── common/
│   ├── financial/
│   └── learning/
└── store/
```

## Implementation Steps

1. **Create new data models** - Define schemas for transactions, budgets, courses, students
2. **Build API endpoints** - RESTful APIs for each module
3. **Implement business logic** - Services for fraud detection, recommendations, etc.
4. **Build frontend** - Vue 3 components with clean UI
5. **Integrate AI** - LLM-powered features (fraud alerts, tutoring, analytics)

## Key Features to Implement

### FinTech Features
- [ ] Transaction categorization
- [ ] Budget creation and tracking
- [ ] Expense analytics dashboard
- [ ] Fraud detection alerts
- [ ] Financial reports generation

### EdTech Features
- [ ] Course creation and management
- [ ] Student enrollment
- [ ] AI-powered tutoring chat
- [ ] Progress tracking
- [ ] Personalized learning paths

## Dependencies to Add

**Backend (Python):**
- SQLAlchemy (database)
- Celery (async tasks)
- More LLM integrations

**Frontend (JS):**
- Chart.js (analytics)
- Pinia (state management)
- Element Plus or similar UI lib

## Timeline

- Week 1: Architecture and data models
- Week 2: Backend API development
- Week 3: Frontend development
- Week 4: Integration and testing

## Notes

- Keep existing MiroFish code archived in case needed later
- Use existing LLM infrastructure (configurable via .env)
- Target both web and mobile-responsive design