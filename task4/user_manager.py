import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Any
from user import User, UserStatus


class UserManager:
    def __init__(self, filename: str = "users.json"):
        self.filename = Path(filename)
        self.users: Dict[int, User] = {}
        self.load_users()

    def save_users(self) -> None:
        users_list = [user.to_dict() for user in self.users.values()]

        self.filename.parent.mkdir(parents=True, exist_ok=True)

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(users_list, f, indent=2, ensure_ascii=False)

    def load_users(self) -> None:
        try:
            if not self.filename.exists():
                return

            with open(self.filename, 'r', encoding='utf-8') as f:
                users_list = json.load(f)

            self.users = {}
            for user_data in users_list:
                user = User.from_dict(user_data)
                self.users[user.user_id] = user
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}


    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def get_by_status(self, status: UserStatus) -> List[User]:
        return [user for user in self.users.values() if user.status == status]

    def get_by_attribute(self, attribute: str, value: Any) -> List[User]:
        result = []
        for user in self.users.values():
            if hasattr(user, attribute):
                attr_value = getattr(user, attribute)
                if attr_value == value:
                    result.append(user)
        return result

    def get_all(self) -> List[User]:
        return list(self.users.values())


    def add_user(self, user: User) -> bool:
        if user.user_id in self.users:
            return False  # User with this ID already exists

        self.users[user.user_id] = user
        self.save_users()
        return True

    def create_user(self, username: str, email: str, status: UserStatus = UserStatus.ACTIVE) -> User:
        # Generate new ID
        new_id = max(self.users.keys()) + 1 if self.users else 1

        user = User(
            user_id=new_id,
            username=username,
            email=email,
            status=status
        )

        self.add_user(user)
        return user


    def delete_by_id(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            self.save_users()
            return True
        return False

    def delete_by_username(self, username: str) -> bool:
        user = self.get_by_username(username)
        if user:
            return self.delete_by_id(user.user_id)
        return False

    def delete_by_status(self, status: UserStatus) -> int:
        users_to_delete = self.get_by_status(status)
        count = 0

        for user in users_to_delete:
            if self.delete_by_id(user.user_id):
                count += 1

        return count

    def delete_by_attribute(self, attribute: str, value: Any) -> int:
        users_to_delete = self.get_by_attribute(attribute, value)
        count = 0

        for user in users_to_delete:
            if self.delete_by_id(user.user_id):
                count += 1

        return count


    def count_users(self) -> int:
        return len(self.users)

    def print_all(self) -> None:
        print("\nВСЕ ПОЛЬЗОВАТЕЛИ")
        for user in self.get_all():
            print(user)
        print(f"Всего: {self.count_users()} пользователей")