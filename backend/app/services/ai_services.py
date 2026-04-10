"""
Finvee Backend - AI Services
Fraud Detection and Learning Recommendations
"""

from typing import List, Dict, Any, Optional
from ..models.financial import FinancialManager, Transaction
from ..models.learning import LearningManager, Course, Enrollment


class FraudDetector:
    """AI-powered fraud detection service"""

    def __init__(self):
        self.rules = {
            "unusual_amount": 10000,  # Single transaction above this
            "unusual_frequency": 10,  # Transactions per hour above this
            "unusual_time": (0, 6),  # Late night hours (0-6 AM)
        }

    def analyze_transaction(
        self, transaction: Transaction, recent_transactions: List[Transaction]
    ) -> Dict[str, Any]:
        """Analyze a single transaction for fraud indicators"""

        score = 0.0
        indicators = []

        # Check amount
        if transaction.amount > self.rules["unusual_amount"]:
            score += 0.4
            indicators.append(f"Unusually high amount: ${transaction.amount}")

        # Check frequency
        hour_ago = transaction.date[:13] + ":00:00"
        recent_count = sum(
            1
            for t in recent_transactions
            if t.date >= hour_ago and t.transaction_id != transaction.transaction_id
        )
        if recent_count > self.rules["unusual_frequency"]:
            score += 0.3
            indicators.append(
                f"High transaction frequency: {recent_count} in last hour"
            )

        # Check time
        hour = int(transaction.date[11:13]) if len(transaction.date) > 11 else 0
        if self.rules["unusual_time"][0] <= hour < self.rules["unusual_time"][1]:
            score += 0.2
            indicators.append(f"Unusual time transaction: {hour}:00")

        # Check category anomalies
        if transaction.category == "Other" and transaction.amount > 500:
            score += 0.1
            indicators.append("High amount in 'Other' category")

        # Check for duplicate amounts (potential testing)
        duplicate_count = sum(
            1
            for t in recent_transactions
            if abs(t.amount - transaction.amount) < 0.01
            and t.transaction_id != transaction.transaction_id
        )
        if duplicate_count >= 3:
            score += 0.2
            indicators.append(f"Multiple similar transactions: {duplicate_count}")

        # Determine if fraudulent
        is_fraudulent = score >= 0.5

        return {
            "transaction_id": transaction.transaction_id,
            "fraud_score": round(score, 2),
            "is_fraudulent": is_fraudulent,
            "indicators": indicators,
            "recommendation": "Review"
            if score >= 0.3
            else "Approve"
            if score < 0.3
            else "Block",
        }

    def analyze_batch(self, transactions: List[Transaction]) -> List[Dict[str, Any]]:
        """Analyze multiple transactions"""
        results = []
        for txn in transactions:
            result = self.analyze_transaction(txn, transactions)
            results.append(result)
        return results


class LearningRecommender:
    """AI-powered learning recommendations"""

    def __init__(self):
        self.categories = {
            "programming": ["Python", "JavaScript", "Java", "Go"],
            "data_science": ["Python", "R", "SQL", "Machine Learning"],
            "business": ["Finance", "Marketing", "Management"],
            "language": ["English", "Spanish", "Chinese", "French"],
            "science": ["Physics", "Chemistry", "Biology", "Math"],
        }

    def recommend_courses(
        self, user_id: str, interests: List[str], skill_level: str = "beginner"
    ) -> List[Dict[str, Any]]:
        """Recommend courses based on user interests and skill level"""

        learning_mgr = LearningManager()

        # Find matching courses
        recommendations = []
        courses = learning_mgr.get_courses(published_only=True)

        for course in courses:
            relevance_score = 0

            # Check category match
            if course.category.lower() in [i.lower() for i in interests]:
                relevance_score += 0.5

            # Check difficulty match
            if course.difficulty == skill_level:
                relevance_score += 0.3

            # Check if already enrolled
            enrollments = learning_mgr.get_enrollments(
                student_id=user_id, course_id=course.course_id
            )
            if enrollments:
                continue  # Skip already enrolled

            if relevance_score > 0:
                recommendations.append(
                    {
                        "course": course.to_dict(),
                        "relevance_score": relevance_score,
                        "reason": self._get_recommendation_reason(course, interests),
                    }
                )

        # Sort by relevance
        recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
        return recommendations[:5]

    def _get_recommendation_reason(self, course: Course, interests: List[str]) -> str:
        """Generate human-readable recommendation reason"""
        if course.category.lower() in [i.lower() for i in interests]:
            return f"Matches your interest in {course.category}"
        if course.difficulty == "beginner":
            return "Perfect for getting started"
        return "Popular among learners"

    def generate_study_plan(
        self, course_id: str, available_hours_per_week: float
    ) -> Dict[str, Any]:
        """Generate a personalized study plan"""

        learning_mgr = LearningManager()
        courses = learning_mgr.get_courses()
        course = next((c for c in courses if c.course_id == course_id), None)

        if not course:
            return {"error": "Course not found"}

        total_hours = course.duration_hours
        weeks = int(total_hours / available_hours_per_week) + 1

        modules = course.modules or []
        modules_per_week = len(modules) / weeks if weeks > 0 else 1

        plan = {
            "course_title": course.title,
            "total_weeks": weeks,
            "hours_per_week": available_hours_per_week,
            "weekly_schedule": [],
        }

        for i in range(min(weeks, 4)):  # Show first 4 weeks
            week_modules = modules[
                int(i * modules_per_week) : int((i + 1) * modules_per_week)
            ]
            plan["weekly_schedule"].append(
                {
                    "week": i + 1,
                    "topics": [m.get("title", "Lesson") for m in week_modules],
                    "estimated_hours": available_hours_per_week,
                }
            )

        return plan


class FinancialAnalyzer:
    """Financial analytics and insights"""

    def get_spending_insights(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """Analyze spending patterns and generate insights"""

        expenses = [t for t in transactions if t.type == "expense"]

        if not expenses:
            return {"message": "No expenses to analyze"}

        # Category breakdown
        category_totals = {}
        for t in expenses:
            category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

        # Top categories
        sorted_categories = sorted(
            category_totals.items(), key=lambda x: x[1], reverse=True
        )

        # Average transaction
        avg_expense = sum(e.amount for e in expenses) / len(expenses)

        # Insights
        insights = []
        if sorted_categories:
            top = sorted_categories[0]
            insights.append(f"You spend most on {top[0]} (${top[1]:.2f})")

        if avg_expense > 100:
            insights.append(
                f"Average expense is ${avg_expense:.2f} - consider budgeting for frequent purchases"
            )

        return {
            "total_expenses": sum(e.amount for e in expenses),
            "transaction_count": len(expenses),
            "average_expense": avg_expense,
            "category_breakdown": dict(sorted_categories),
            "top_category": sorted_categories[0][0] if sorted_categories else None,
            "insights": insights,
        }

    def compare_periods(
        self, current: List[Transaction], previous: List[Transaction]
    ) -> Dict[str, Any]:
        """Compare current period with previous"""

        current_total = sum(t.amount for t in current if t.type == "expense")
        previous_total = sum(t.amount for t in previous if t.type == "expense")

        change = current_total - previous_total
        change_percent = (change / previous_total * 100) if previous_total > 0 else 0

        return {
            "current_period_total": current_total,
            "previous_period_total": previous_total,
            "change": change,
            "change_percent": round(change_percent, 1),
            "trend": "up" if change > 0 else "down" if change < 0 else "stable",
        }
