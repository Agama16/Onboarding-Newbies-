import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from typing import Dict, Any
from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def valid_order() -> Dict[str, Any]:
    return {
        "customer_name": "bob",
        "pizzas": ["Margherita", 10.0],
    }


@pytest.fixture
def invalid_order() -> Dict[str, Any]:
    return {
        "customer_name": "john",
        "pizzas": ["none", 1.0],
    }


@pytest.fixture
def empty_order() -> Dict[str, Any]:
    return {
        "customer_name": "testOrder",
        "pizzas": [],
    }


@pytest.fixture
def mock_save_db(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    monkeypatch.setattr("main.save_order_to_db", mock)
    return mock


def test_get_menu(client: TestClient) -> None:
    response = client.get("/menu")

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "Margherita"


def test_create_order_success(
        client: TestClient,
        valid_order: Dict[str, Any],
        mock_save_db: MagicMock,) -> None:
    mock_save_db.return_value = True

    response = client.post("/order", json=valid_order)

    assert response.status_code == 200
    mock_save_db.assert_called_once()


def test_create_order_fail_nonexistent_item(
        client: TestClient,
        invalid_order: Dict[str, Any],
        mock_save_db: MagicMock,) -> None:
    mock_save_db.return_value = False

    response = client.post("/order", json=invalid_order)

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "could not save the order, check that the order's details are valid and try again"
    )

    mock_save_db.assert_called_once()


def test_create_order_fail_empty_list(
        client: TestClient,
        empty_order: Dict[str, Any],) -> None:
    response = client.post("/order", json=empty_order)

    assert response.status_code == 400
    assert response.json()["detail"] == "list is empty"
