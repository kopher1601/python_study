class BankAccount:
    def __init__(self, owner: str, balance: int = 0):
        if balance < 0:
            raise ValueError("초기 잔액은 음수일 수 없습니다.")

        self.owner = owner
        self._balance = balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("입금액은 0보다 커야 합니다.")

        self._balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("출금액은 0보다 커야 합니다.")

        if amount > self._balance:
            raise ValueError("잔액이 부족합니다.")

        self._balance -= amount

    def get_balance(self) -> int:
        return self._balance


account = BankAccount(owner="Yun", balance=10_000)
account.deposit(5_000)
account.withdraw(3_000)

print(account.get_balance())

