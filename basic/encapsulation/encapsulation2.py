from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Order:
    def __init__(self, order_id: str, total_price: int) -> None:
        if not order_id:
            raise ValueError("주문 ID 는 비어 있을 수 없습니다.")

        if total_price <= 0:
            raise ValueError("주문 금액은 0보다 커야 합니다.")

        self._order_id = order_id
        self._total_price = total_price
        self._status = OrderStatus.PENDING

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def total_price(self) -> int:
        return self._total_price

    @property
    def status(self) -> OrderStatus:
        return self._status

    def pay(self, paid_amount: int) -> None:
        if self._status is not OrderStatus.PENDING:
            raise ValueError("결제 대기 상태의 주문만 결제할 수 있습니다.")

        if paid_amount != self._total_price:
            raise ValueError("결제 금액이 주문 금액과 일치하지 않습니다.")

        self._status = OrderStatus.PAID

    def cancel(self) -> None:
        if self._status is OrderStatus.PAID:
            raise ValueError("결제된 주문은 취소할 수 없습니다.")

        if self._status is OrderStatus.CANCELLED:
            raise ValueError("이미 취소된 주문은 취소할 수 없습니다.")

        self._status = OrderStatus.CANCELLED


order = Order(order_id="ORDER-001", total_price=30_000)
order.pay(paid_amount=30_000)

print(order.status)

