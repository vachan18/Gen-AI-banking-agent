"""
Unit and Integration Tests for Yellow.ai Banking Webhook & API Service.
Validates banking endpoints, payload structure, error handling, and webhook logic.
"""

import json
import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from webhook_server import app, load_banking_data


@pytest.fixture
def client():
    """Flask test client fixture."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_endpoint(client):
    """Test root endpoint returns service metadata and endpoints."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "online"
    assert "endpoints" in data
    assert "/api/health" in data["endpoints"]
    assert "/api/loans" in data["endpoints"]


def test_health_check(client):
    """Test health check returns 200 healthy."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_load_banking_data_structure():
    """Test underlying JSON database loader."""
    data = load_banking_data()
    assert "customer" in data
    assert "accounts" in data
    assert "loans" in data
    assert "recent_transactions" in data
    assert data["customer"]["name"] == "Vachan U S"


def test_get_loan_accounts_carousel(client):
    """Test loan retrieval and carousel card formatting for Yellow.ai."""
    response = client.get("/api/loans")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["total_loans"] >= 2
    assert len(data["carousel_items"]) == data["total_loans"]

    # Verify first carousel item structure
    card = data["carousel_items"][0]
    assert "title" in card
    assert "subtitle" in card
    assert "value" in card
    assert len(card["actions"]) > 0
    assert card["actions"][0]["type"] == "postback"


def test_get_loan_details_success(client):
    """Test loan detail lookup for valid loan ID (case-insensitive)."""
    for loan_id in ["LN001", "ln001"]:
        response = client.get(f"/api/loans/{loan_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["loan"]["loan_id"] == "LN001"
        assert "summary_text" in data
        assert "Outstanding Balance" in data["summary_text"]


def test_get_loan_details_not_found(client):
    """Test loan detail lookup for non-existent loan ID returns 404."""
    response = client.get("/api/loans/LN999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"
    assert "not found" in data["message"].lower()


def test_get_accounts(client):
    """Test account balance lookup."""
    response = client.get("/api/accounts")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert len(data["accounts"]) > 0
    assert data["accounts"][0]["currency"] == "INR"


def test_get_transactions(client):
    """Test transaction history retrieval."""
    response = client.get("/api/transactions")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["transactions"], list)
    assert len(data["transactions"]) > 0


def test_webhook_action_loan_summary(client):
    """Test Yellow.ai webhook routing: get_loan_summary."""
    payload = {
        "event": "message",
        "data": {
            "action": "get_loan_summary",
            "loan_id": "LN002"
        }
    }
    response = client.post(
        "/webhook/yellowai",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["loan"]["loan_id"] == "LN002"
    assert data["loan"]["loan_type"] == "Personal Loan"


def test_webhook_action_fetch_balance(client):
    """Test Yellow.ai webhook routing: fetch_balance."""
    payload = {
        "event": "user_intent",
        "data": {
            "action": "fetch_balance"
        }
    }
    response = client.post(
        "/webhook/yellowai",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "accounts" in data


def test_webhook_action_fetch_transactions(client):
    """Test Yellow.ai webhook routing: fetch_transactions."""
    payload = {
        "event": "user_intent",
        "data": {
            "action": "fetch_transactions"
        }
    }
    response = client.post(
        "/webhook/yellowai",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "transactions" in data


def test_webhook_unhandled_action_echo(client):
    """Test Yellow.ai webhook default fallback behavior."""
    payload = {
        "event": "custom_event",
        "data": {
            "action": "unhandled_custom_action",
            "key": "value"
        }
    }
    response = client.post(
        "/webhook/yellowai",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["received_action"] == "unhandled_custom_action"
