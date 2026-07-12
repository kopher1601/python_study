from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: int) -> None:
        """지정한 금액을 결제한다."""


class CreditCardPayment(PaymentMethod):
    def pay(self, amount: int) -> None:
        print(f"신용카드로 {amount:,}원을 결제합니다.")

class BankTransferPayment(PaymentMethod):
    def pay(self, amount: int) -> None:
        print(f"계좌이체로 {amount:,}원을 결제합니다.")

class PointPayment(PaymentMethod):
    def pay(self, amount: int) -> None:
        print(f"포인트 {amount:,}점을 사용합니다.")

class KakaoPay:
    """duck typing"""
    def pay(self, amount:int) -> None:
        print(f"카카오페이로 {amount:,}원을 결제합니다.")

def checkout(payment_method: PaymentMethod, amount: int) -> None:
    payment_method.pay(amount)


card = CreditCardPayment()
transfer = BankTransferPayment()
point = PointPayment()
kakao_pay = KakaoPay()

checkout(card, 10_000)
checkout(transfer, 20_000)
checkout(point, 100)
checkout(kakao_pay, 30_000)


