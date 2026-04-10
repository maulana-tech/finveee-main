"""
Finvee Backend - Financial Models
Transaction, Budget, Account, and Financial Analytics
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import uuid
import json


def generate_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


CATEGORY_EXPENSE = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Bills & Utilities",
    "Health",
    "Education",
    "Travel",
    "Other",
]

CATEGORY_INCOME = ["Salary", "Investment", "Gift", "Business", "Refund", "Other"]


@dataclass
class Account:
    account_id: str
    user_id: str
    name: str
    account_type: str  # checking, savings, credit, investment
    balance: float = 0.0
    currency: str = "USD"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,
            "name": self.name,
            "account_type": self.account_type,
            "balance": self.balance,
            "currency": self.currency,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
        }


@dataclass
class Transaction:
    transaction_id: str
    user_id: str
    account_id: str
    type: str  # income, expense
    amount: float
    category: str
    description: str
    date: str
    tags: List[str] = field(default_factory=list)
    is_fraudulent: bool = False
    fraud_score: Optional[float] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "account_id": self.account_id,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "tags": self.tags,
            "is_fraudulent": self.is_fraudulent,
            "fraud_score": self.fraud_score,
            "created_at": self.created_at,
        }


@dataclass
class Budget:
    budget_id: str
    user_id: str
    category: str
    amount: float
    period: str  # weekly, monthly, yearly
    start_date: str
    end_date: str
    spent: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "budget_id": self.budget_id,
            "user_id": self.user_id,
            "category": self.category,
            "amount": self.amount,
            "period": self.period,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "spent": self.spent,
            "created_at": self.created_at,
        }


@dataclass
class FinancialReport:
    report_id: str
    user_id: str
    report_type: str  # monthly, yearly, custom
    start_date: str
    end_date: str
    total_income: float
    total_expense: float
    net_savings: float
    category_breakdown: Dict[str, float]
    trends: Dict[str, Any]
    insights: List[str]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "report_id": self.report_id,
            "user_id": self.user_id,
            "report_type": self.report_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_income": self.total_income,
            "total_expense": self.total_expense,
            "net_savings": self.net_savings,
            "category_breakdown": self.category_breakdown,
            "trends": self.trends,
            "insights": self.insights,
            "created_at": self.created_at,
        }


class FinancialManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = {
                "accounts": {},
                "transactions": {},
                "budgets": {},
                "reports": {},
            }
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        import os

        data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        data_file = os.path.join(data_dir, "financial.json")

        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                self._data = json.load(f)

    def _save_data(self):
        import os

        data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        os.makedirs(data_dir, exist_ok=True)
        data_file = os.path.join(data_dir, "financial.json")

        with open(data_file, "w") as f:
            json.dump(self._data, f, indent=2)

    def create_account(
        self,
        user_id: str,
        name: str,
        account_type: str,
        initial_balance: float = 0.0,
        currency: str = "USD",
    ) -> Account:
        account = Account(
            account_id=generate_id("acc_"),
            user_id=user_id,
            name=name,
            account_type=account_type,
            balance=initial_balance,
            currency=currency,
        )
        self._data["accounts"][account.account_id] = account.to_dict()
        self._save_data()
        return account

    def get_accounts(self, user_id: str) -> List[Account]:
        return [
            Account(**acc)
            for acc in self._data["accounts"].values()
            if acc["user_id"] == user_id and acc["is_active"]
        ]

    def create_transaction(
        self,
        user_id: str,
        account_id: str,
        trans_type: str,
        amount: float,
        category: str,
        description: str,
        date: str,
        tags: List[str] = None,
    ) -> Transaction:
        transaction = Transaction(
            transaction_id=generate_id("txn_"),
            user_id=user_id,
            account_id=account_id,
            type=trans_type,
            amount=amount,
            category=category,
            description=description,
            date=date,
            tags=tags or [],
        )

        # Update account balance
        account = self._data["accounts"].get(account_id)
        if account:
            if trans_type == "income":
                account["balance"] += amount
            else:
                account["balance"] -= amount
            account["updated_at"] = datetime.now().isoformat()

        self._data["transactions"][transaction.transaction_id] = transaction.to_dict()
        self._save_data()
        return transaction

    def get_transactions(
        self,
        user_id: str,
        account_id: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> List[Transaction]:
        transactions = [
            Transaction(**t)
            for t in self._data["transactions"].values()
            if t["user_id"] == user_id
        ]

        if account_id:
            transactions = [t for t in transactions if t.account_id == account_id]
        if start_date:
            transactions = [t for t in transactions if t.date >= start_date]
        if end_date:
            transactions = [t for t in transactions if t.date <= end_date]

        return sorted(transactions, key=lambda x: x.date, reverse=True)

    def create_budget(
        self,
        user_id: str,
        category: str,
        amount: float,
        period: str,
        start_date: str,
        end_date: str,
    ) -> Budget:
        budget = Budget(
            budget_id=generate_id("bud_"),
            user_id=user_id,
            category=category,
            amount=amount,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )
        self._data["budgets"][budget.budget_id] = budget.to_dict()
        self._save_data()
        return budget

    def get_budgets(self, user_id: str) -> List[Budget]:
        return [
            Budget(**b)
            for b in self._data["budgets"].values()
            if b["user_id"] == user_id
        ]

    def update_budget_spent(self, budget_id: str, spent: float):
        if budget_id in self._data["budgets"]:
            self._data["budgets"][budget_id]["spent"] = spent
            self._save_data()

    def generate_report(
        self, user_id: str, report_type: str, start_date: str, end_date: str
    ) -> FinancialReport:
        transactions = self.get_transactions(
            user_id, start_date=start_date, end_date=end_date
        )

        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expense = sum(t.amount for t in transactions if t.type == "expense")

        category_breakdown = {}
        for t in transactions:
            if t.type == "expense":
                category_breakdown[t.category] = (
                    category_breakdown.get(t.category, 0) + t.amount
                )

        # Generate insights
        insights = []
        if total_expense > total_income * 0.8:
            insights.append(
                "Your expenses are high relative to income. Consider reducing discretionary spending."
            )
        if category_breakdown:
            top_category = max(category_breakdown, key=category_breakdown.get)
            insights.append(
                f"Highest spending category: {top_category} (${category_breakdown[top_category]:.2f})"
            )

        report = FinancialReport(
            report_id=generate_id("rpt_"),
            user_id=user_id,
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            total_income=total_income,
            total_expense=total_expense,
            net_savings=total_income - total_expense,
            category_breakdown=category_breakdown,
            trends={"month_over_month": "neutral"},
            insights=insights,
        )

        self._data["reports"][report.report_id] = report.to_dict()
        self._save_data()
        return report

    def get_reports(self, user_id: str) -> List[FinancialReport]:
        return [
            FinancialReport(**r)
            for r in self._data["reports"].values()
            if r["user_id"] == user_id
        ]
