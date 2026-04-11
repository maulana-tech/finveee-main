<template>
  <div class="home-container">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-brand">FINVEE</div>
      <div class="nav-links">
        <a href="#features" class="nav-link">Features</a>
        <a href="#simulation" class="nav-link">Simulation</a>
        <a href="#about" class="nav-link">About</a>
        <router-link to="/login" class="nav-link login-link">Login</router-link>
        <router-link to="/register" class="nav-link cta-link">Get Started</router-link>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="tag-row">
          <span class="orange-tag">AI-POWERED</span>
          <span class="version-text">Version 1.0</span>
        </div>
        
        <h1 class="main-title">
          Master Your Finance<br>
          <span class="gradient-text">Accelerate Your Learning</span>
        </h1>
        
        <div class="hero-desc">
          <p>
            Finvee combines powerful financial management tools with 
            personalized AI-driven education. Track expenses, detect fraud, 
            learn new skills - all in one platform.
          </p>
        </div>
        
        <div class="hero-cta">
          <router-link to="/register" class="cta-btn primary">
            Start Free <span class="btn-arrow">-&gt;</span>
          </router-link>
          <router-link to="/login" class="cta-btn secondary">
            Demo Login
          </router-link>
        </div>
        
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-line"></span>
            <span class="stat-number">3</span>
            <span class="stat-label">Modules</span>
          </div>
          <div class="stat-item">
            <span class="stat-line"></span>
            <span class="stat-number">AI</span>
            <span class="stat-label">Powered</span>
          </div>
          <div class="stat-item">
            <span class="stat-line"></span>
            <span class="stat-number">SWARM</span>
            <span class="stat-label">Intelligence</span>
          </div>
        </div>
      </div>
      
      <div class="hero-visual">
        <div class="feature-card">
          <div class="card-header">
            <span class="card-icon">$</span>
            <span class="card-accent"></span>
          </div>
          <div class="card-title">FinTech AI</div>
          <div class="card-features">
            <span>- Fraud Detection</span>
            <span>- Budget Planning</span>
            <span>- Analytics</span>
          </div>
          <div class="card-footer"></div>
        </div>
        <div class="feature-card">
          <div class="card-header">
            <span class="card-icon">#</span>
            <span class="card-accent"></span>
          </div>
          <div class="card-title">EdTech AI</div>
          <div class="card-features">
            <span>- AI Tutoring</span>
            <span>- Progress Tracking</span>
            <span>- Course Management</span>
          </div>
          <div class="card-footer"></div>
        </div>
        <div class="feature-card accent">
          <div class="card-header">
            <span class="card-icon">[S]</span>
            <span class="card-accent"></span>
          </div>
          <div class="card-title">Swarm AI</div>
          <div class="card-features">
            <span>- Multi-Agent Sim</span>
            <span>- Reality Mapping</span>
            <span>- Prediction Engine</span>
          </div>
          <div class="card-footer"></div>
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="section-header">
        <span class="section-line"></span>
        <span class="section-title">Features</span>
        <span class="section-line"></span>
      </div>
      
      <div class="features-grid">
        <!-- FinTech Features -->
        <div class="feature-group">
          <h2 class="group-title">Financial Management</h2>
          <div class="feature-list">
            <div class="feature-item">
              <span class="feature-icon">[B]</span>
              <div class="feature-text">
                <h3>Multi-Account Support</h3>
                <p>Manage checking, savings, credit cards, and investments in one place</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[T]</span>
              <div class="feature-text">
                <h3>Smart Transactions</h3>
                <p>Track income and expenses with automatic categorization</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[P]</span>
              <div class="feature-text">
                <h3>Budget Planning</h3>
                <p>Create budgets with spending limits and progress tracking</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[F]</span>
              <div class="feature-text">
                <h3>AI Fraud Detection</h3>
                <p>Real-time transaction monitoring with risk scoring</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[A]</span>
              <div class="feature-text">
                <h3>Spending Analytics</h3>
                <p>Visual insights and AI-powered recommendations</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- EdTech Features -->
        <div class="feature-group">
          <h2 class="group-title">AI-Powered Learning</h2>
          <div class="feature-list">
            <div class="feature-item">
              <span class="feature-icon">[C]</span>
              <div class="feature-text">
                <h3>Course Management</h3>
                <p>Create and publish educational courses with structured modules</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[E]</span>
              <div class="feature-text">
                <h3>Enrollment System</h3>
                <p>Track learner progress and course completion</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[S]</span>
              <div class="feature-text">
                <h3>AI Tutoring</h3>
                <p>Interactive chat with AI-powered learning assistant</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[R]</span>
              <div class="feature-text">
                <h3>Progress Tracking</h3>
                <p>Monitor learning journey with detailed analytics</p>
              </div>
            </div>
            <div class="divider-thin"></div>
            <div class="feature-item">
              <span class="feature-icon">[L]</span>
              <div class="feature-text">
                <h3>Personalized Recommendations</h3>
                <p>AI-suggested courses based on your interests</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <!-- Swarm Intelligence Section -->
    <section id="simulation" class="swarm-section">
      <div class="section-header">
        <span class="section-line"></span>
        <span class="section-title">Swarm Intelligence Engine</span>
        <span class="section-line"></span>
      </div>

      <div class="swarm-content">
        <div class="swarm-intro">
          <h2>Create a Swarm Intelligence Mirror That Maps Reality</h2>
          <p>
            Predict outcomes by simulating thousands of AI agents in a parallel digital world. 
            Extract seed information from real world events - breaking news, policy drafts, 
            financial signals - and watch as intelligent agents with independent personalities, 
            long-term memory, and behavioral logic interact and evolve.
          </p>
          <p class="swarm-tagline">
            Rehearse the future in a digital sandbox, win decisions after countless simulations.
          </p>
        </div>

        <div class="swarm-stats">
          <div class="swarm-stat">
            <span class="swarm-number">1000+</span>
            <span class="swarm-label">AI Agents</span>
          </div>
          <div class="swarm-stat">
            <span class="swarm-number">Multi</span>
            <span class="swarm-label">Platform Sim</span>
          </div>
          <div class="swarm-stat">
            <span class="swarm-number">Real</span>
            <span class="swarm-label">Reality Mapping</span>
          </div>
          <div class="swarm-stat">
            <span class="swarm-number">AI</span>
            <span class="swarm-label">Prediction</span>
          </div>
        </div>

        <div class="workflow-section">
          <div class="workflow-title">WORKFLOW_STEPS</div>
          <div class="workflow-grid">
            <div class="workflow-step">
              <span class="step-num">01</span>
              <span class="step-title">GRAPH_BUILD</span>
              <span class="step-desc">Extract seed info & build knowledge graph</span>
            </div>
            <div class="workflow-step">
              <span class="step-num">02</span>
              <span class="step-title">ENV_SETUP</span>
              <span class="step-desc">Configure agents & environment</span>
            </div>
            <div class="workflow-step">
              <span class="step-num">03</span>
              <span class="step-title">SIMULATION</span>
              <span class="step-desc">Run multi-agent simulation</span>
            </div>
            <div class="workflow-step">
              <span class="step-num">04</span>
              <span class="step-title">REPORT</span>
              <span class="step-desc">Generate prediction report</span>
            </div>
            <div class="workflow-step">
              <span class="step-num">05</span>
              <span class="step-title">INTERACTION</span>
              <span class="step-desc">Chat with agents & explore</span>
            </div>
          </div>
        </div>

        <div class="swarm-cta">
          <router-link to="/process/new" class="cta-btn primary">
            Start Simulation <span class="btn-arrow">-&gt;</span>
          </router-link>
        </div>
      </div>
    </section>

    <div class="section-divider"></div>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>Ready to Get Started?</h2>
        <p>Join thousands of users managing their finances and learning with AI</p>
        <div class="cta-buttons">
          <router-link to="/register" class="cta-btn primary">Create Free Account</router-link>
          <router-link to="/login" class="cta-btn secondary">Login as Demo</router-link>
        </div>
        <p class="demo-hint">Demo: demo@finvee.com / demo123</p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-line"></div>
      <div class="footer-content">
        <div class="footer-brand">FINVEE</div>
        <div class="footer-links">
          <span>&copy; 2026 Finvee. All rights reserved.</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Home page for Finvee
</script>

<style scoped>
/* CSS Variables */
:root {
  --black: #000000;
  --white: #ffffff;
  --orange: #ff4500;
  --gray-light: #f5f5f5;
  --gray-text: #666666;
  --gray-border: #cccccc;
  --border: #cccccc;
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: var(--white);
  font-family: var(--font-sans);
  color: var(--black);
}

/* Navbar */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, var(--orange), transparent);
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 2px;
  font-size: 1.3rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  transition: opacity 0.2s;
}

.nav-link:hover {
  opacity: 0.8;
}

.login-link {
  padding: 6px 16px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 4px;
}

.cta-link {
  background: var(--orange);
  padding: 8px 20px;
  border-radius: 4px;
  font-weight: 600;
}

.cta-link:hover {
  background: #ff6a00;
}

/* Hero Section */
.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 80px 40px;
  gap: 60px;
}

.hero-content {
  flex: 1;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
}

.version-text {
  color: #999;
  font-weight: 500;
}

.main-title {
  font-size: 3.5rem;
  line-height: 1.2;
  font-weight: 700;
  margin: 0 0 30px 0;
  letter-spacing: -1px;
}

.gradient-text {
  background: linear-gradient(90deg, var(--orange) 0%, #ff6a00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-desc {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 500px;
  margin-bottom: 40px;
}

.hero-cta {
  display: flex;
  gap: 16px;
  margin-bottom: 50px;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 0.95rem;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.2s;
}

.cta-btn.primary {
  background: var(--orange);
  color: var(--white);
}

.cta-btn.primary:hover {
  background: #ff6a00;
  transform: translateY(-2px);
}

.cta-btn.secondary {
  background: transparent;
  color: var(--black);
  border: 2px solid var(--gray-border);
}

.cta-btn.secondary:hover {
  border-color: var(--black);
}

.hero-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stat-number {
  font-family: var(--font-mono);
  font-size: 2rem;
  font-weight: 700;
  color: var(--orange);
}

.stat-label {
  font-size: 0.85rem;
  color: var(--gray-text);
  margin-top: 4px;
}

.stat-line {
  width: 30px;
  height: 2px;
  background: var(--gray-border);
  margin-bottom: 8px;
}

/* Hero Visual */
.hero-visual {
  flex: 0.9;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-card {
  padding: 24px;
  background: var(--white);
  border: 2px solid var(--gray-border);
  border-radius: 8px;
  position: relative;
}

.feature-card.accent {
  border-color: var(--orange);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-icon {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--black);
}

.feature-card.accent .card-icon {
  color: var(--orange);
}

.card-accent {
  width: 40px;
  height: 1px;
  background: var(--gray-border);
}

.card-title {
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 12px;
  color: var(--black);
}

.card-features {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--gray-text);
}

.card-footer {
  margin-top: 16px;
  height: 1px;
  background: var(--gray-border);
}

/* Section Divider */
.section-divider {
  height: 2px;
  background: var(--gray-border);
  max-width: 1400px;
  margin: 0 auto;
}

/* Features Section */
.features-section {
  padding: 80px 40px;
  background: var(--white);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 50px;
}

.section-line {
  flex: 1;
  max-width: 100px;
  height: 2px;
  background: var(--gray-border);
}

.section-title {
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--gray-text);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 60px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-group {
  background: var(--white);
  padding: 40px;
  border: 2px solid var(--gray-border);
  border-radius: 8px;
}

.group-title {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 30px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--gray-border);
}

.feature-list {
  display: flex;
  flex-direction: column;
}

.feature-item {
  display: flex;
  gap: 16px;
  padding: 16px 0;
}

.feature-icon {
  font-family: var(--font-mono);
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--orange);
  min-width: 30px;
}

.feature-text h3 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: var(--black);
}

.feature-text p {
  font-size: 0.85rem;
  color: var(--gray-text);
  margin: 0;
  line-height: 1.5;
}

.divider-thin {
  height: 1px;
  background: var(--gray-border);
}

/* Swarm Section */
.swarm-section {
  padding: 80px 40px;
  background: var(--gray-light);
}

.swarm-content {
  max-width: 1200px;
  margin: 0 auto;
}

.swarm-intro {
  text-align: center;
  margin-bottom: 50px;
}

.swarm-intro h2 {
  font-family: var(--font-mono);
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 20px 0;
  color: var(--black);
}

.swarm-intro p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 800px;
  margin: 0 auto 20px;
}

.swarm-tagline {
  font-family: var(--font-mono);
  font-size: 1rem;
  color: var(--orange);
  font-weight: 600;
}

.swarm-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 50px;
}

.swarm-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 40px;
  background: var(--white);
  border: 2px solid var(--gray-border);
}

.swarm-number {
  font-family: var(--font-mono);
  font-size: 2rem;
  font-weight: 700;
  color: var(--orange);
}

.swarm-label {
  font-size: 0.85rem;
  color: var(--gray-text);
  margin-top: 8px;
}

.workflow-section {
  margin-bottom: 40px;
}

.workflow-title {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--gray-text);
  letter-spacing: 1px;
  margin-bottom: 20px;
  text-align: center;
}

.workflow-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.workflow-step {
  background: var(--white);
  border: 2px solid var(--gray-border);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.step-num {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  color: var(--orange);
}

.step-title {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  margin: 8px 0 4px;
}

.step-desc {
  font-size: 0.7rem;
  color: var(--gray-text);
}

.swarm-cta {
  text-align: center;
}

/* CTA Section */
.cta-section {
  padding: 100px 40px;
  background: var(--black);
  color: var(--white);
  text-align: center;
  position: relative;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--orange), transparent);
}

.cta-content h2 {
  font-size: 2.5rem;
  margin: 0 0 16px 0;
}

.cta-content p {
  font-size: 1.1rem;
  color: #999;
  margin-bottom: 40px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 24px;
}

.cta-buttons .cta-btn {
  padding: 16px 32px;
}

.demo-hint {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: #666;
}

/* Footer */
.footer {
  padding: 30px 40px;
  background: var(--white);
}

.footer-line {
  height: 2px;
  background: var(--gray-border);
  margin-bottom: 30px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.footer-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 2px;
}

.footer-links {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* Responsive */
@media (max-width: 1024px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-visual {
    width: 100%;
  }
  
  .hero-desc {
    margin: 0 auto 40px;
  }
  
  .hero-cta {
    justify-content: center;
  }
  
  .hero-stats {
    justify-content: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }

  .workflow-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 0 20px;
  }
  
  .hero-section {
    padding: 40px 20px;
  }
  
  .main-title {
    font-size: 2.5rem;
  }
  
  .hero-visual {
    flex-direction: column;
  }

  .swarm-stats {
    flex-wrap: wrap;
  }

  .workflow-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
}
</style>