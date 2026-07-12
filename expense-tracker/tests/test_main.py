from collections.abc import Iterator

import pytest
from starlette import status
from starlette.testclient import TestClient

from app.main import app, transactions

client = TestClient(app=app)


@pytest.fixture(autouse=True)
def clear_transactions() -> Iterator[None]:
    transactions.clear()

    yield

    transactions.clear()


def create_sample_transaction() -> dict:
    return {
        "title": "점심 식사",
        "amount": 12_000,
        "transaction_type": "expense",
        "category": "식비",
        "occurred_at": "2026-07-12",
    }


def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Expense Tracker API"}


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_transaction() -> None:
    response = client.post("/transactions", json=create_sample_transaction())

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        **create_sample_transaction(),
    }


def test_create_transaction_with_negative_amount() -> None:
    request_body = create_sample_transaction()
    request_body["amount"] = -1_000

    response = client.post("/transactions", json=request_body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_transactions() -> None:
    client.post(
        "/transactions",
        json=create_sample_transaction(),
    )

    response = client.get("/transactions")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "점심 식사"


def test_get_transaction() -> None:
    create_response = client.post(
        "/transactions",
        json=create_sample_transaction(),
    )
    transaction_id = create_response.json()["id"]

    response = client.get(f"/transactions/{transaction_id}")

    assert response.status_code == 200
    assert response.json()["id"] == transaction_id
    assert response.json()["amount"] == 12000


def test_get_nonexistent_transaction() -> None:
    response = client.get("/transactions/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "거래 내역을 찾을 수 없습니다",
    }


def test_update_transaction() -> None:
    create_response = client.post(
        "/transactions",
        json=create_sample_transaction(),
    )
    transaction_id = create_response.json()["id"]

    update_data = {
        "title": "저녁 식사",
        "amount": 25000,
        "transaction_type": "expense",
        "category": "식비",
        "occurred_at": "2026-07-12",
    }

    response = client.put(
        f"/transactions/{transaction_id}",
        json=update_data,
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": transaction_id,
        **update_data,
    }


def test_delete_transaction() -> None:
    create_response = client.post(
        "/transactions",
        json=create_sample_transaction(),
    )
    transaction_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/transactions/{transaction_id}",
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/transactions/{transaction_id}",
    )

    assert get_response.status_code == 404
