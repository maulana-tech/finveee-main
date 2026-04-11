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


# ============== Import/Export Routes ==============


@financial_bp.route("/transactions/export", methods=["GET"])
def export_transactions():
    """Export transactions to CSV"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        account_id = request.args.get("account_id")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        from ..models.financial import FinancialManager
        from ..services.import_export import ImportExporter

        fm = FinancialManager()
        transactions = fm.get_transactions(
            user_id, account_id=account_id, start_date=start_date, end_date=end_date
        )

        csv_content = ImportExporter.export_transactions_csv(transactions)

        return jsonify(
            {"success": True, "data": csv_content, "filename": "transactions.csv"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/transactions/import", methods=["POST"])
def import_transactions():
    """Import transactions from CSV"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()
        csv_content = data.get("csv_content", "")
        account_id = data.get("account_id")

        if not account_id:
            return jsonify({"success": False, "error": "Account ID required"}), 400

        from ..services.import_export import ImportExporter
        from ..models.financial import FinancialManager

        result = ImportExporter.import_transactions_csv(
            csv_content, user_id, account_id
        )

        if not result["imported"]:
            return jsonify(
                {
                    "success": False,
                    "error": "No valid transactions to import",
                    "details": result["errors"],
                }
            ), 400

        # Create transactions
        fm = FinancialManager()
        created = []
        for item in result["imported"]:
            txn = fm.create_transaction(
                user_id=user_id,
                account_id=account_id,
                trans_type=item["type"],
                amount=item["amount"],
                category=item["category"],
                description=item["description"],
                date=item["date"],
                tags=item.get("tags", []),
            )
            created.append(txn.to_dict())

        return jsonify(
            {
                "success": True,
                "data": {
                    "imported": len(created),
                    "errors": result["errors"],
                    "transactions": created,
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/budgets/export", methods=["GET"])
def export_budgets():
    """Export budgets to CSV"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.financial import FinancialManager
        from ..services.import_export import ImportExporter

        fm = FinancialManager()
        budgets = fm.get_budgets(user_id)

        csv_content = ImportExporter.export_budgets_csv(budgets)

        return jsonify(
            {"success": True, "data": csv_content, "filename": "budgets.csv"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/budgets/import", methods=["POST"])
def import_budgets():
    """Import budgets from CSV"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()
        csv_content = data.get("csv_content", "")

        from ..services.import_export import ImportExporter
        from ..models.financial import FinancialManager

        result = ImportExporter.import_budgets_csv(csv_content, user_id)

        if not result["imported"]:
            return jsonify(
                {
                    "success": False,
                    "error": "No valid budgets to import",
                    "details": result["errors"],
                }
            ), 400

        fm = FinancialManager()
        created = []
        for item in result["imported"]:
            # Default dates if not provided
            start = item.get("start_date") or datetime.now().isoformat()[:10]
            end = item.get("end_date") or datetime.now().isoformat()[:10]

            budget = fm.create_budget(
                user_id=user_id,
                category=item["category"],
                amount=item["amount"],
                period=item["period"],
                start_date=start,
                end_date=end,
            )
            created.append(budget.to_dict())

        return jsonify(
            {
                "success": True,
                "data": {
                    "imported": len(created),
                    "errors": result["errors"],
                    "budgets": created,
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/accounts/export", methods=["GET"])
def export_accounts():
    """Export accounts to CSV"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.financial import FinancialManager
        from ..services.import_export import ImportExporter

        fm = FinancialManager()
        accounts = fm.get_accounts(user_id)

        csv_content = ImportExporter.export_accounts_csv(accounts)

        return jsonify(
            {"success": True, "data": csv_content, "filename": "accounts.csv"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/accounts/import", methods=["POST"])
def import_accounts():
    """Import accounts from CSV"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()
        csv_content = data.get("csv_content", "")

        from ..services.import_export import ImportExporter
        from ..models.financial import FinancialManager

        result = ImportExporter.import_accounts_csv(csv_content, user_id)

        if not result["imported"]:
            return jsonify(
                {
                    "success": False,
                    "error": "No valid accounts to import",
                    "details": result["errors"],
                }
            ), 400

        fm = FinancialManager()
        created = []
        for item in result["imported"]:
            account = fm.create_account(
                user_id=user_id,
                name=item["name"],
                account_type=item["account_type"],
                initial_balance=item.get("balance", 0),
                currency=item.get("currency", "USD"),
            )
            created.append(account.to_dict())

        return jsonify(
            {
                "success": True,
                "data": {
                    "imported": len(created),
                    "errors": result["errors"],
                    "accounts": created,
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/sample-csv/<csv_type>", methods=["GET"])
def get_sample_csv(csv_type: str):
    """Get sample CSV template"""
    try:
        from ..services.import_export import ImportExporter

        sample = ImportExporter.generate_sample_csv(csv_type)

        return jsonify({"success": True, "data": sample, "type": csv_type})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/transactions/export/excel", methods=["GET"])
def export_transactions_excel():
    """Export transactions to Excel"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        account_id = request.args.get("account_id")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        from ..models.financial import FinancialManager
        from ..services.import_export import ImportExporter

        fm = FinancialManager()
        transactions = fm.get_transactions(
            user_id, account_id=account_id, start_date=start_date, end_date=end_date
        )

        excel_data = ImportExporter.export_transactions_excel(transactions)

        from flask import send_file
        from io import BytesIO

        return send_file(
            BytesIO(excel_data),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="transactions.xlsx",
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/budgets/export/excel", methods=["GET"])
def export_budgets_excel():
    """Export budgets to Excel"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.financial import FinancialManager
        from ..services.import_export import ImportExporter

        fm = FinancialManager()
        budgets = fm.get_budgets(user_id)

        excel_data = ImportExporter.export_budgets_excel(budgets)

        from flask import send_file
        from io import BytesIO

        return send_file(
            BytesIO(excel_data),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="budgets.xlsx",
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@financial_bp.route("/accounts/export/excel", methods=["GET"])
def export_accounts_excel():
    """Export accounts to Excel"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.financial import FinancialManager
        from ..services.import_export import ImportExporter

        fm = FinancialManager()
        accounts = fm.get_accounts(user_id)

        excel_data = ImportExporter.export_accounts_excel(accounts)

        from flask import send_file
        from io import BytesIO

        return send_file(
            BytesIO(excel_data),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="accounts.xlsx",
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
