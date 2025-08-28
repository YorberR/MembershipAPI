from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("name") == "Prueba"


def test_read_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json().get("id")
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json().get("name") == "Prueba"


def test_read_customer_not_found(client):
    response_read = client.get(f"/customers/123")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND
    assert response_read.json().get("detail") == "Customer not found"


def test_delete_customer_not_found(client):
    response_read = client.delete(f"/customers/123")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND
    assert response_read.json().get("detail") == "Customer not found"


def test_update_customer_not_found(client):
    response_read = client.patch(
        f"/customers/123",
        json={"name": "Prueba2"},
    )
    assert response_read.status_code == status.HTTP_404_NOT_FOUND
    assert response_read.json().get("detail") == "Customer not found"
