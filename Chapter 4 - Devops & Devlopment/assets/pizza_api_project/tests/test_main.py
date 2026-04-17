from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from typing import Any, Dict
from main import app

client: TestClient = TestClient(app)


def test_get_menu() -> None:
    response = client.get("/menu")

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "Margherita"


@patch("main.save_order_to_db")
def test_create_order_success(mock_save_db: MagicMock) -> None:
    
    mock_order: Dict[str, Any] = {
        "customer_name": "bob",
        "pizzas": ["Margherita", 10.0],
    }
    mock_save_db.return_value = True

    response = client.post("/order", json=mock_order)
    assert response.status_code == 200


@patch("main.save_order_to_db")
def test_create_order_fail_nonexistent_item(mock_save_db: MagicMock) -> None:
    
    mock_order: Dict[str, Any] = {
        "customer_name": "john",
        "pizzas": ["none", 1.0],
    }
    mock_save_db.return_value = False
    
    response = client.post("/order", json=mock_order)
    assert response.status_code == 400
    assert response.json()["detail"] == "order failed"


def test_create_order_fail_empty_list() -> None:
    
    order: Dict[str, Any] = {
        "customer_name": "testOrder",
        "pizzas": [],
    }

    response = client.post("/order", json=order)
    assert response.status_code == 400
    assert response.json()["detail"] == "list is empty"
    
