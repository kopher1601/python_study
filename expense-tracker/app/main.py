from datetime import date
from enum import Enum

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Expense Tracker API",
    description="개인 지출 관리 학습 프로젝트",
    version="0.0.1",
)


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: int = Field(gt=0)
    transaction_type: TransactionType
    category: str = Field(min_length=1, max_length=50)
    occurred_at: date


class Transaction(TransactionCreate):
    id: int


transactions: list[Transaction] = []


def generate_transaction_id() -> int:
    return (
        max(
            (transaction.id for transaction in transactions),
            default=0,
        )
        + 1
    )


def find_transaction(transaction_id: int) -> Transaction:
    for transaction in transactions:
        if transaction.id == transaction_id:
            return transaction

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="거래 내역을 찾을 수 없습니다",
    )


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Expense Tracker API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/transactions",
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(data: TransactionCreate) -> Transaction:
    transaction = Transaction(
        id=generate_transaction_id(),
        **data.model_dump(),
    )

    transactions.append(transaction)

    return transaction


@app.get(
    "/transactions",
    response_model=list[Transaction],
)
def get_transactions() -> list[Transaction]:
    return transactions


@app.get(
    "/transactions/{transaction_id}",
    response_model=Transaction,
)
def get_transaction(transaction_id: int) -> Transaction:
    return find_transaction(transaction_id)


@app.put(
    "/transactions/{transaction_id}",
    response_model=Transaction,
)
def update_transaction(
    transaction_id: int,
    data: TransactionCreate,
) -> Transaction:
    find_transaction(transaction_id)

    updated_transaction = Transaction(
        id=transaction_id,
        **data.model_dump(),
    )

    for index, transaction in enumerate(transactions):
        if transaction.id == transaction_id:
            transactions[index] = updated_transaction
            break

    return updated_transaction


@app.delete(
    "/transactions/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transaction(transaction_id: int) -> Response:
    transaction = find_transaction(transaction_id)
    transactions.remove(transaction)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
