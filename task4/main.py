from user_manager import UserManager


def main():
    print("=" * 40)
    print("ПРОСТАЯ СИСТЕМА УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ")
    print("=" * 40)

    manager = UserManager()

    print("\n1. Создаем пользователей:")

    # Первый способ - создать через create_user
    user1 = manager.create_user("аня", "anya@mail.ru")
    print(f"   Создан: {user1}")

    user2 = manager.create_user("вася", "vasya@mail.ru")
    user2.status = "inactive"  # Меняем статус
    print(f"   Создан: {user2}")

    user3 = manager.create_user("петя", "petya@mail.ru")
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
    inactive_users = manager.get_by_status("inactive")
    print(f"   Неактивных пользователей: {len(inactive_users)}")

    # 5. Удаляем пользователей
    print("\n3. Удаляем пользователей:")

    # По ID
    if manager.delete_by_id(3):
        print("   Удалили пользователя с ID 3")

    # По имени
    if manager.delete_by_username("аня"):
        print("   Удалили пользователя 'аня'")

    print("\n4. Результат после удаления:")
    manager.print_all()

    print("\n" + "=" * 40)
    print("Все данные сохранены в файле 'users.json'")
    print("=" * 40)


if __name__ == "__main__":
    main()