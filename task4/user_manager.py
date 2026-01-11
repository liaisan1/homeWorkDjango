import json
from user import User

class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = {}
        self.load_users()

    def save_users(self):
        users_list = []
        for user in self.users.values():
            users_list.append({
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "status": user.status
            })

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(users_list, f, indent=2, ensure_ascii=False)

    def load_users(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                users_list = json.load(f)

            self.users = {}
            for user_data in users_list:
                user = User(
                    user_data["user_id"],
                    user_data["username"],
                    user_data["email"],
                    user_data["status"]
                )
                self.users[user.user_id] = user
        except:
            pass

    def get_by_id(self, user_id):
        return self.users.get(user_id)

    def get_by_username(self, username):
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    # По статусу
    def get_by_status(self, status):
        result = []
        for user in self.users.values():
            if user.status == status:
                result.append(user)
        return result

    # Все пользователи
    def get_all(self):
        return list(self.users.values())


    def add_user(self, user):
        if user.user_id in self.users:
            return False  # Уже есть такой ID

        self.users[user.user_id] = user
        self.save_users()
        return True

    def create_user(self, username, email):
        # Находим максимальный ID и добавляем 1
        if self.users:
            new_id = max(self.users.keys()) + 1
        else:
            new_id = 1

        user = User(new_id, username, email)
        self.add_user(user)
        return user


    def delete_by_id(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            self.save_users()
            return True
        return False

    def delete_by_username(self, username):
        user = self.get_by_username(username)
        if user:
            return self.delete_by_id(user.user_id)
        return False

    def delete_by_status(self, status):
        users_to_delete = self.get_by_status(status)
        count = 0

        for user in users_to_delete:
            if self.delete_by_id(user.user_id):
                count += 1

        return count


    def count_users(self):
        return len(self.users)

    def print_all(self):
        print("\n=== ВСЕ ПОЛЬЗОВАТЕЛИ ===")
        for user in self.get_all():
            print(user)
        print(f"Всего: {self.count_users()} пользователей")