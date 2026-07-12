from typing import Protocol

# Protocol 의 의미 : 클래스의 이름이나 상속 관계는 중요하지 않다. 이 형태의 동작을 제공하면 된다.

class PaymentMethod(Protocol):
    def pay(self, amount: int) -> None:
        ...

class KakaoPay:
    def pay(self, amount: int) -> None:
        print(f"카카오페이로 {amount:,}원을 결제합니다.")

def checkout(payment_method: PaymentMethod, amount: int) -> None:
    payment_method.pay(amount)

checkout(KakaoPay(), 30_000)