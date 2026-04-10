<div align="center">

<img src="./static/image/MiroFish_logo_compressed.jpeg" alt="Finvee Logo" width="50%"/>

# Finvee

**AI-Powered Finance & Learning Platform**

*Smart financial management meets personalized education*

</div>

## Overview

**Finvee** is a unified platform combining FinTech AI and EdTech AI to help users manage their finances and accelerate their learning journey.

### FinTech Features
- **Account Management** - Track multiple bank accounts, credit cards, investments
- **Transaction Tracking** - Record and categorize income/expenses with AI analysis
- **Budget Planning** - Create budgets with spending limits and alerts
- **Spending Analytics** - Visual insights and AI-powered recommendations
- **Fraud Detection** - Real-time transaction monitoring and risk scoring

### EdTech Features
- **Course Management** - Create and publish educational courses
- **Student Enrollment** - Track learner progress and completion
- **AI Tutoring** - Interactive chat with AI-powered learning assistant
- **Progress Tracking** - Monitor learning journey with detailed analytics
- **Personalized Recommendations** - AI-suggested courses based on interests

## Quick Start

### Prerequisites

| Tool | Version | Description |
|------|---------|-------------|
| **Node.js** | 18+ | Frontend runtime |
| **Python** | ≥3.11 | Backend runtime |
| **uv** | Latest | Python package manager |

### 1. Configure Environment

```bash
cp .env.example .env
```

**Required Variables:**
```env
# LLM API (optional - for AI features)
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4
```

### 2. Install Dependencies

```bash
npm run setup:all
```

### 3. Start Services

```bash
npm run dev
```

**Service URLs:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

## Tech Stack

- **Frontend**: Vue 3 + Vite
- **Backend**: Flask (Python)
- **Database**: JSON file storage (demo) / SQLAlchemy (production)
- **AI**: OpenAI-compatible LLM integration

## Project Structure

```
finveee-main/
├── backend/
│   ├── app/
│   │   ├── api/          # REST API endpoints
│   │   ├── models/       # Data models
│   │   └── services/     # Business logic
│   └── run.py            # Backend entry
├── frontend/
│   └── src/
│       ├── views/        # Page components
│       ├── components/   # Reusable components
│       └── api/          # API client
└── package.json           # Project scripts
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Financial
- `GET/POST /api/financial/accounts` - Manage accounts
- `GET/POST /api/financial/transactions` - Manage transactions
- `GET/POST /api/financial/budgets` - Manage budgets
- `GET /api/financial/analytics/insights` - AI spending insights
- `POST /api/financial/transactions/analyze` - Fraud detection

### Learning
- `GET/POST /api/learning/courses` - Manage courses
- `GET/POST /api/learning/enrollments` - Student enrollment
- `GET/POST /api/learning/tutoring` - AI tutoring sessions
- `GET /api/learning/recommendations` - Course recommendations
- `GET /api/learning/study-plan/<course_id>` - Personalized study plan

## License

AGPL-3.0

---

*Built with AI-powered features for modern finance and education*