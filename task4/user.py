class User:
    def __init__(self, user_id, username, email, status="active"):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.status = status

    def __str__(self):
        return f"ID: {self.user_id}, Имя: {self.username}, Email: {self.email}"