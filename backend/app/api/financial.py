"""
Finvee Backend - Financial API Routes
"""

from flask import Blueprint, request, jsonify
import traceback

financial_bp = Blueprint("financial", __name__)


@financial_bp.route("/accounts", methods=["GET"])
def get_accounts():
    """Get all accounts for the user"""
    try:
        from ..models.user import UserManager
        from ..models.financial import FinancialManager

        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        fm = FinancialManager()
        accounts = fm.get_accounts(user_id)

        return jsonify({"success": True, "data": [a.to_dict() for a in accounts]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/accounts", methods=["POST"])
def create_account():
    """Create a new account"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.financial import FinancialManager

        fm = FinancialManager()

        account = fm.create_account(
            user_id=user_id,
            name=data.get("name"),
            account_type=data.get("account_type", "checking"),
            initial_balance=data.get("initial_balance", 0.0),
            currency=data.get("currency", "USD"),
        )

        return jsonify({"success": True, "data": account.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/transactions", methods=["GET"])
def get_transactions():
    """Get transactions with optional filters"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        account_id = request.args.get("account_id")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        from ..models.financial import FinancialManager

        fm = FinancialManager()

        transactions = fm.get_transactions(
            user_id=user_id,
            account_id=account_id,
            start_date=start_date,
            end_date=end_date,
        )

        return jsonify({"success": True, "data": [t.to_dict() for t in transactions]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/transactions", methods=["POST"])
def create_transaction():
    """Create a new transaction"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.financial import FinancialManager
        from ..services.ai_services import FraudDetector

        fm = FinancialManager()

        # Create transaction
        transaction = fm.create_transaction(
            user_id=user_id,
            account_id=data.get("account_id"),
            trans_type=data.get("type"),
            amount=float(data.get("amount")),
            category=data.get("category"),
            description=data.get("description", ""),
            date=data.get("date"),
            tags=data.get("tags", []),
        )

        # Run fraud detection
        recent_txns = fm.get_transactions(user_id)
        fraud_detector = FraudDetector()
        fraud_result = fraud_detector.analyze_transaction(transaction, recent_txns)

        # Update transaction with fraud info
        transaction.is_fraudulent = fraud_result["is_fraudulent"]
        transaction.fraud_score = fraud_result["fraud_score"]

        return jsonify(
            {
                "success": True,
                "data": transaction.to_dict(),
                "fraud_check": fraud_result,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/transactions/analyze", methods=["POST"])
def analyze_transactions():
    """Analyze transactions for fraud"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()
        transaction_ids = data.get("transaction_ids", [])

        from ..models.financial import FinancialManager
        from ..services.ai_services import FraudDetector

        fm = FinancialManager()
        all_transactions = fm.get_transactions(user_id)

        # Filter to requested transactions
        transactions = [
            t for t in all_transactions if t.transaction_id in transaction_ids
        ]

        fraud_detector = FraudDetector()
        results = fraud_detector.analyze_batch(transactions)

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/budgets", methods=["GET"])
def get_budgets():
    """Get all budgets"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.financial import FinancialManager

        fm = FinancialManager()

        budgets = fm.get_budgets(user_id)

        # Calculate spent amounts
        from datetime import datetime

        now = datetime.now().isoformat()[:10]

        for budget in budgets:
            transactions = fm.get_transactions(
                user_id=user_id, start_date=budget.start_date, end_date=budget.end_date
            )
            expenses = [
                t
                for t in transactions
                if t.type == "expense" and t.category == budget.category
            ]
            budget.spent = sum(e.amount for e in expenses)

        return jsonify({"success": True, "data": [b.to_dict() for b in budgets]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/budgets", methods=["POST"])
def create_budget():
    """Create a new budget"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.financial import FinancialManager

        fm = FinancialManager()

        budget = fm.create_budget(
            user_id=user_id,
            category=data.get("category"),
            amount=float(data.get("amount")),
            period=data.get("period", "monthly"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
        )

        return jsonify({"success": True, "data": budget.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/reports", methods=["GET"])
def get_reports():
    """Get financial reports"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.financial import FinancialManager

        fm = FinancialManager()

        reports = fm.get_reports(user_id)

        return jsonify({"success": True, "data": [r.to_dict() for r in reports]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/reports/generate", methods=["POST"])
def generate_report():
    """Generate a new financial report"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.financial import FinancialManager

        fm = FinancialManager()

        report = fm.generate_report(
            user_id=user_id,
            report_type=data.get("report_type", "monthly"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
        )

        return jsonify({"success": True, "data": report.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/analytics/insights", methods=["GET"])
def get_spending_insights():
    """Get spending insights"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        from ..models.financial import FinancialManager
        from ..services.ai_services import FinancialAnalyzer

        fm = FinancialManager()
        transactions = fm.get_transactions(
            user_id, start_date=start_date, end_date=end_date
        )

        analyzer = FinancialAnalyzer()
        insights = analyzer.get_spending_insights(transactions)

        return jsonify({"success": True, "data": insights})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
