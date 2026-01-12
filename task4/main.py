from user_manager import UserManager
from user import User, UserStatus


def main():
    print("=" * 40)
    print("ПРОСТАЯ СИСТЕМА УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ")
    print("=" * 40)

    manager = UserManager()

    print("\n1. Создаем пользователей:")

    # Создаем пользователей
    user1 = manager.create_user("аня", "anya@mail.ru")
    print(f"   Создан: {user1}")

    user2 = manager.create_user("вася", "vasya@mail.ru", UserStatus.INACTIVE)
    print(f"   Создан: {user2}")

    user3 = manager.create_user("петя", "petya@mail.ru", UserStatus.ACTIVE)
    print(f"   Создан: {user3}")

    manager.print_all()

    print("\n2. Ищем пользователей:")

    # По ID
    found = manager.get_by_id(1)
    if found:
        print(f"   Найден по ID 1: {found.username}")

    # По имени
    found = manager.get_by_username("вася")
    if found:
        print(f"   Найден по имени 'вася': {found.email}")

    # По статусу
    inactive_users = manager.get_by_status(UserStatus.INACTIVE)
    print(f"   Неактивных пользователей: {len(inactive_users)}")

    # По любому атрибуту (email)
    email_users = manager.get_by_attribute("email", "petya@mail.ru")
    print(f"   Пользователей с email 'petya@mail.ru': {len(email_users)}")

    print("\n3. Удаляем пользователей:")

    # По ID
    if manager.delete_by_id(3):
        print("   Удалили пользователя с ID 3")

    # По имени
    if manager.delete_by_username("аня"):
        print("   Удалили пользователя 'аня'")

    # По статусу
    deleted_count = manager.delete_by_status(UserStatus.INACTIVE)
    print(f"   Удалили {deleted_count} неактивных пользователей")

    print("\n4. Результат после удаления:")
    manager.print_all()

    # Демонстрация добавления пользователя напрямую
    print("\n5. Добавляем пользователя напрямую:")
    new_user = User(
        user_id=100,
        username="мария",
        email="maria@example.com",
        status=UserStatus.BANNED
    )
    if manager.add_user(new_user):
        print(f"   Добавлен: {new_user}")

    print("\n" + "=" * 40)
    print("Все данные сохранены в файле 'users.json'")
    print("=" * 40)


if __name__ == "__main__":
    main()