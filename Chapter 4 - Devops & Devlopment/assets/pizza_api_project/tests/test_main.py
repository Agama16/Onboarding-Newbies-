from fastapi.testclient import TestClient
from main import app
from models.pizza import OrderRequest
from unittest.mock import patch

client = TestClient(app)

def test_get_menu():
    response = client.get("/menu")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "Margherita"

# create a mock test
@patch('main.save_order_to_db')
def test_create_order_success(mock_save_db):

    # the mock order
    mock_order={
        "customer_name" : "bob",
        "pizzas" : [ "Margherita", 10.0]
    }

    # create success return value on purpose
    mock_save_db.return_value = True

    # make sure the wanted outcome is satisfied
    response = client.post('/order', mock_order)
    assert response.status_code == 200
    

@patch('main.save_order_to_db')
def test_create_order_fail(mock_save_db):  

    mock_order={
        "customer_name" : "john", "pizzas" : [ "none", 1.0]
    }

    # create failure on purpose
    mock_save_db.return_value = False

    response = client.post('/order', mock_order)
    assert response.status_code == 400
    assert response.detail == "order failed"

def test_create_order_empty_list():

    """TODO: Test that sending an order with no pizzas returns a 400 error."""
    #create an empty list order
    order = OrderRequest("testOrder", [])
    response = client.post("/order", json=order)
    assert response.status_code == 400
    assert response.detail == "list is empty"


