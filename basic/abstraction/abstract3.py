from dataclasses import dataclass
from typing import Protocol


@dataclass
class User:
    id: int
    name: str

class UserRepository(Protocol):
    def save(self, user:User) -> None:
        ...

    def find_by_id(self, user_id: int) -> User | None:
        ...

class MemoryUserRepository:
    def __init__(self):
        self._users: dict[int, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def find_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def register(self, user_id: int, name: str) -> User:
        if not name.strip():
            raise ValueError("이름은 비어 있을 수 없습니다")

        if self._repository.find_by_id(user_id) is not None:
            raise ValueError("이미 존재하는 사용자입니다")

        user = User(id=user_id, name=name)
        self._repository.save(user)
        return user


repository = MemoryUserRepository()
service = UserService(repository)

user = service.register(1, "John")
print(user)

