from flask import Blueprint, jsonify, request
import json
import os

simulation_bp = Blueprint("simulation", __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SIMULATION_DATA_FILE = os.path.join(DATA_DIR, "simulation_entities.json")


def load_simulation_data():
    try:
        with open(SIMULATION_DATA_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading simulation data: {e}")
        return {"companies": [], "individuals": [], "simulation_scenarios": []}


@simulation_bp.route("/entities", methods=["GET"])
def get_entities():
    data = load_simulation_data()
    entity_type = request.args.get("type")

    if entity_type == "company":
        return jsonify({"success": True, "data": data.get("companies", [])})
    elif entity_type == "individual":
        return jsonify({"success": True, "data": data.get("individuals", [])})
    else:
        return jsonify(
            {
                "success": True,
                "data": {
                    "companies": data.get("companies", []),
                    "individuals": data.get("individuals", []),
                },
            }
        )


@simulation_bp.route("/entities/<entity_id>", methods=["GET"])
def get_entity(entity_id):
    data = load_simulation_data()

    for company in data.get("companies", []):
        if company["entity_id"] == entity_id:
            return jsonify({"success": True, "data": company})

    for individual in data.get("individuals", []):
        if individual["entity_id"] == entity_id:
            return jsonify({"success": True, "data": individual})

    return jsonify({"success": False, "error": "Entity not found"}), 404


@simulation_bp.route("/scenarios", methods=["GET"])
def get_scenarios():
    data = load_simulation_data()
    return jsonify({"success": True, "data": data.get("simulation_scenarios", [])})


@simulation_bp.route("/scenarios/<scenario_id>", methods=["GET"])
def get_scenario(scenario_id):
    data = load_simulation_data()

    for scenario in data.get("simulation_scenarios", []):
        if scenario["scenario_id"] == scenario_id:
            return jsonify({"success": True, "data": scenario})

    return jsonify({"success": False, "error": "Scenario not found"}), 404


@simulation_bp.route("/run", methods=["POST"])
def run_simulation():
    data = request.get_json()

    entity_ids = data.get("entity_ids", [])
    scenario_id = data.get("scenario_id")
    rounds = data.get("rounds", 10)

    simulation_data = load_simulation_data()

    selected_entities = []
    for entity_id in entity_ids:
        for company in simulation_data.get("companies", []):
            if company["entity_id"] == entity_id:
                selected_entities.append(company)
        for individual in simulation_data.get("individuals", []):
            if individual["entity_id"] == entity_id:
                selected_entities.append(individual)

    scenario = None
    for s in simulation_data.get("simulation_scenarios", []):
        if s["scenario_id"] == scenario_id:
            scenario = s
            break

    if not scenario:
        return jsonify({"success": False, "error": "Scenario not found"}), 404

    results = simulate_entities(selected_entities, scenario, rounds)

    return jsonify(
        {
            "success": True,
            "data": {
                "scenario": scenario,
                "entities": selected_entities,
                "results": results,
            },
        }
    )


def simulate_entities(entities, scenario, rounds):
    results = []

    gdp_growth = scenario["parameters"]["GDP_growth"]
    unemployment = scenario["parameters"]["unemployment_increase"]
    interest = scenario["parameters"]["interest_rate_change"]
    inflation = scenario["parameters"]["inflation_rate"]

    for entity in entities:
        entity_result = {
            "entity_id": entity["entity_id"],
            "name": entity["name"],
            "type": entity["type"],
            "rounds": [],
        }

        if entity["type"] == "company":
            base_revenue = entity["financial_data"].get("revenue_2023", 0)
            base_profit = entity["financial_data"].get("profit_2023", 0)
            base_customers = entity["metrics"].get("customer_count", 0)
            base_churn = entity["metrics"].get("churn_rate", 0)

            for round_num in range(1, rounds + 1):
                impact_factor = 1 + (gdp_growth * 0.5)

                if gdp_growth < 0:
                    revenue_change = gdp_growth * base_revenue * (round_num / rounds)
                    profit_change = (
                        gdp_growth * base_profit * (round_num / rounds) * 1.5
                    )
                    churn_change = base_churn * (unemployment * round_num / rounds)
                else:
                    revenue_change = gdp_growth * base_revenue * (round_num / rounds)
                    profit_change = gdp_growth * base_profit * (round_num / rounds)
                    churn_change = -base_churn * 0.3 * (round_num / rounds)

                projected_revenue = max(0, base_revenue + revenue_change)
                projected_profit = max(-base_profit * 0.5, base_profit + profit_change)
                projected_customers = max(0, int(base_customers * (1 + churn_change)))

                entity_result["rounds"].append(
                    {
                        "round": round_num,
                        "revenue": int(projected_revenue),
                        "profit": int(projected_profit),
                        "customers": projected_customers,
                        "health_score": calculate_health_score(
                            projected_profit, revenue_change, inflation, interest
                        ),
                    }
                )

        else:
            base_income = entity["financial_data"].get("income_annual", 0)
            base_savings = entity["financial_data"].get("savings", 0)
            base_debt = entity["financial_data"].get("debt", 0)
            credit_score = entity["financial_data"].get("credit_score", 650)

            for round_num in range(1, rounds + 1):
                impact_factor = 1 + (gdp_growth * 0.3)

                if gdp_growth < 0:
                    income_change = (
                        gdp_growth * base_income * 0.8 * (round_num / rounds)
                    )
                    savings_change = (
                        gdp_growth * base_savings * (unemployment * round_num / rounds)
                    )
                    debt_pressure = interest * base_debt * (round_num / rounds)
                else:
                    income_change = gdp_growth * base_income * (round_num / rounds)
                    savings_change = (
                        gdp_growth * base_savings * 0.5 * (round_num / rounds)
                    )
                    debt_pressure = interest * base_debt * (round_num / rounds)

                projected_income = max(0, base_income + income_change)
                projected_savings = max(0, base_savings + savings_change)
                projected_debt = base_debt + debt_pressure

                credit_impact = (inflation - interest) * 50 * (round_num / rounds)
                projected_credit = min(850, max(300, credit_score + credit_impact))

                entity_result["rounds"].append(
                    {
                        "round": round_num,
                        "income": int(projected_income),
                        "savings": int(projected_savings),
                        "debt": int(projected_debt),
                        "credit_score": int(projected_credit),
                        "health_score": calculate_health_score_individual(
                            projected_income, projected_savings, projected_debt
                        ),
                    }
                )

        results.append(entity_result)

    return results


def calculate_health_score(profit, revenue_change, inflation, interest):
    score = 50

    if profit > 0:
        score += 20
    else:
        score -= 20

    if revenue_change > 0:
        score += 15
    elif revenue_change < 0:
        score -= 15

    if inflation > interest:
        score -= 10
    else:
        score += 10

    return max(0, min(100, score))


def calculate_health_score_individual(income, savings, debt):
    score = 50

    savings_rate = savings / max(1, income)
    if savings_rate > 0.3:
        score += 25
    elif savings_rate > 0.1:
        score += 10
    else:
        score -= 15

    debt_to_income = debt / max(1, income)
    if debt_to_income < 0.3:
        score += 20
    elif debt_to_income < 0.5:
        score += 5
    else:
        score -= 20

    return max(0, min(100, score))
