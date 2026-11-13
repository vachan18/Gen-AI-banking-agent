"""
AI Banking Agent - Webhook & API Integration Service
Backend microservice handling banking operations, API integrations,
and webhook calls for the Yellow.ai GenAI Banking Assistant.
"""

import json
import logging
import os
from datetime import datetime
from flask import Flask, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("yellowai-banking-service")

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "mock_banking_data.json")


def load_banking_data() -> dict:
    """Load mock banking records."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Data file not found at {DATA_PATH}")
        return {"customer": {}, "accounts": [], "loans": [], "recent_transactions": []}


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Yellow.ai Gen AI Banking Assistant API",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoints": [
            "/api/health",
            "/api/loans",
            "/api/loans/<loan_id>",
            "/api/accounts",
            "/api/transactions",
            "/webhook/yellowai"
        ]
    }), 200


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/loans", methods=["GET", "POST"])
def get_loan_accounts():
    """
    Endpoint: getLoanAccounts
    Used by Yellow.ai flow routing to fetch customer active loans
    and populate carousel cards (Home Loan LN001, Personal Loan LN002).
    """
    data = load_banking_data()
    loans = data.get("loans", [])
    
    # Format response suitable for Yellow.ai dynamic quick replies / carousel cards
    cards = []
    for loan in loans:
        cards.append({
            "title": loan["loan_type"],
            "subtitle": f"Loan ID: {loan['loan_id']} | Outstanding: INR {loan['outstanding_balance']:,.2f}",
            "value": loan["loan_id"],
            "actions": [
                {
                    "title": f"Select {loan['loan_type']}",
                    "type": "postback",
                    "payload": {
                        "selected_loan_id": loan["loan_id"],
                        "loan_type": loan["loan_type"]
                    }
                }
            ]
        })
    
    return jsonify({
        "status": "success",
        "customer_id": data.get("customer", {}).get("customer_id"),
        "total_loans": len(loans),
        "loans": loans,
        "carousel_items": cards
    }), 200


@app.route("/api/loans/<loan_id>", methods=["GET"])
def get_loan_details(loan_id: str):
    """
    Fetch specific loan information based on loan ID selection.
    Matches condition checks in Yellow.ai workflow (LN001 vs LN002).
    """
    data = load_banking_data()
    loans = data.get("loans", [])
    matched = next((l for l in loans if l["loan_id"].upper() == loan_id.upper()), None)
    
    if not matched:
        return jsonify({
            "status": "error",
            "message": f"Loan ID '{loan_id}' not found."
        }), 404

    return jsonify({
        "status": "success",
        "loan": matched,
        "summary_text": (
            f"Here are the details for your {matched['loan_type']} ({matched['loan_id']}):\n"
            f"• Outstanding Balance: INR {matched['outstanding_balance']:,.2f}\n"
            f"• Monthly EMI: INR {matched['emi_amount']:,.2f}\n"
            f"• Interest Rate: {matched['interest_rate']}%\n"
            f"• Remaining EMIs: {matched['remaining_emis']}\n"
            f"• Next Due Date: {matched['next_due_date']}"
        )
    }), 200


@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    """Fetch customer savings/checking account balance and details."""
    data = load_banking_data()
    return jsonify({
        "status": "success",
        "customer": data.get("customer"),
        "accounts": data.get("accounts")
    }), 200


@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    """Fetch recent transaction history."""
    data = load_banking_data()
    return jsonify({
        "status": "success",
        "transactions": data.get("recent_transactions", [])
    }), 200


@app.route("/webhook/yellowai", methods=["POST"])
def yellow_ai_webhook():
    """
    Yellow.ai Webhook Handler.
    Receives JSON events, intent context, and slot variables from Yellow.ai bots,
    executes backend business logic, and returns structured responses.
    """
    payload = request.get_json(silent=True) or {}
    logger.info(f"Received Yellow.ai webhook event: {payload.get('event', 'unknown')}")

    event = payload.get("event")
    data_payload = payload.get("data", {})
    action = data_payload.get("action")

    if action == "get_loan_summary":
        loan_id = data_payload.get("loan_id", "LN001")
        return get_loan_details(loan_id)
    elif action == "fetch_balance":
        return get_accounts()
    elif action == "fetch_transactions":
        return get_transactions()

    return jsonify({
        "status": "success",
        "message": "Webhook processed successfully",
        "received_action": action,
        "echo": data_payload
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Yellow.ai Banking Webhook Service on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
