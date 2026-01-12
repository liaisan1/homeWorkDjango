"""Start module with tests for entity manager using User model."""

from typing import Any, List

from models.post import Post, PostStatus
from models.user import User, UserStatus


def print_check(title: str, expected: int, items: List[Any]):
    ok = len(items) == expected
    print(
        f"{title}: expected={expected}, got={len(items)} -> {'PASS' if ok else 'FAIL'}"
    )
    for it in items:
        print("  ", it)


def test_users():
    print("\nTESTING USERS\n")
    # Добавление
    try:
        u1 = User(username="alice", password="pass1", status=UserStatus.CREATED)
        u2 = User(username="bob", password="pass2", status=UserStatus.CREATED)
        User.objects.add([u1, u2])
        User.objects.save()
        print("Added 2 users")
    except Exception as e:
        print("Add failed:", e)

    # Получить все
    try:
        all_items = User.objects.get()
        print_check("After add", 2, all_items)
    except Exception as e:
        print("Get all failed:", e)

    # Получить по критерию
    try:
        alice = User.objects.get({"username": "alice"})
        print_check("Get by username=alice", 1, alice)
    except Exception as e:
        print("Get by criteria failed:", e)

    # Обновление
    try:
        updated = User.objects.update({"username": "bob"}, {"password": "newpass"})
        print_check("Update bob password (returned)", 1, updated)
        bob = User.objects.get({"username": "bob"})
        print_check("Verify bob after update", 1, bob)
    except Exception as e:
        print("Update failed:", e)

    # __getitem__ (если поддерживается)
    try:
        by_username = User.objects[{"username": "bob"}]
        print_check("Get by username using __getitem__", 1, by_username)
    except Exception:
        pass

    # Удаление по критерию
    try:
        deleted = User.objects.delete({"username": "alice"})
        print_check("Delete alice", 1, deleted)
    except Exception as e:
        print("Delete failed:", e)

    # Удалить все
    try:
        User.objects.delete(None)
        empty = User.objects.get()
        print_check("After delete all", 0, empty)
        User.objects.save()
    except Exception as e:
        print("Delete all failed:", e)


def test_posts():
    print("\n=== TESTING POSTS ===\n")

    # Добавление постов
    try:
        p1 = Post(
            title="First Post",
            description="Introduction to ORM",
            text="This is the first post about ORM patterns",
            status=PostStatus.CREATED,
        )
        p2 = Post(
            title="Second Post",
            description="Advanced topics",
            text="This post covers advanced ORM features",
            status=PostStatus.PUBLISHED,
        )
        p3 = Post(
            title="Third Post",
            description="Best practices",
            text="Follow these best practices for ORM",
            status=PostStatus.CREATED,
        )
        Post.objects.add([p1, p2, p3])
        Post.objects.save()
        print("Added 3 posts")
    except Exception as e:
        print("Add posts failed:", e)

    # Получить все посты
    try:
        all_posts = Post.objects.get()
        print_check("After add posts", 3, all_posts)
    except Exception as e:
        print("Get all posts failed:", e)

    # Получить по статусу
    try:
        created_posts = Post.objects.get({"status": PostStatus.CREATED})
        print_check("Get posts with status CREATED", 2, created_posts)
    except Exception as e:
        print("Get by status failed:", e)

    # Получить по заголовку
    try:
        first_post = Post.objects.get({"title": "First Post"})
        print_check("Get post by title", 1, first_post)
    except Exception as e:
        print("Get by title failed:", e)

    # Обновление статуса поста
    try:
        updated = Post.objects.update(
            {"title": "First Post"}, {"status": PostStatus.PUBLISHED}
        )
        print_check("Update First Post status (returned)", 1, updated)
        published_posts = Post.objects.get({"status": PostStatus.PUBLISHED})
        print_check("Verify published posts count", 2, published_posts)
    except Exception as e:
        print("Update post failed:", e)

    # __getitem__ для постов
    try:
        by_title = Post.objects[{"title": "Second Post"}]
        print_check("Get post by title using __getitem__", 1, by_title)
    except Exception:
        pass

    # Обновление нескольких полей
    try:
        updated = Post.objects.update(
            {"title": "Third Post"},
            {"description": "Updated description", "status": PostStatus.PUBLISHED},
        )
        print_check("Update multiple fields (returned)", 1, updated)
    except Exception as e:
        print("Update multiple fields failed:", e)

    # Удаление поста по критерию
    try:
        deleted = Post.objects.delete({"title": "Second Post"})
        print_check("Delete Second Post", 1, deleted)
        remaining = Post.objects.get()
        print_check("Posts after deletion", 2, remaining)
    except Exception as e:
        print("Delete post failed:", e)

    # Удалить все посты
    try:
        Post.objects.delete(None)
        empty = Post.objects.get()
        print_check("After delete all posts", 0, empty)
        Post.objects.save()
    except Exception as e:
        print("Delete all posts failed:", e)


def test_enum_serialization():
    print("\n=== TESTING ENUM SERIALIZATION ===\n")

    try:
        user = User(username="test", password="test", status=UserStatus.BANNED)

        # Проверяем to_dict()
        user_dict = user.to_dict()
        print(f"to_dict() result: {user_dict}")
        print(f"Type of status in dict: {type(user_dict['status'])}")
        print(f"Value of status in dict: {user_dict['status']}")

        # Проверяем from_dict()
        user2 = User.from_dict(user_dict)
        print(f"\nfrom_dict() result: {user2}")
        print(f"Type of status in object: {type(user2.status)}")
        print(f"Value of status in object: {user2.status}")
        print(f"Status equals original: {user2.status == UserStatus.BANNED}")

        # Тест с JSON
        user_json = user.to_json()
        print(f"\nto_json() result: {user_json}")

        user3 = User.from_json(user_json)
        print(f"from_json() result: {user3}")

        # Тест с Post
        post = Post(
            title="Test Post",
            description="Test",
            text="Test text",
            status=PostStatus.DELETED
        )

        post_dict = post.to_dict()
        print(f"\nPost to_dict(): {post_dict}")

        post2 = Post.from_dict(post_dict)
        print(f"Post from_dict(): {post2}")
        print(f"Post status correct: {post2.status == PostStatus.DELETED}")

    except Exception as e:
        print(f"Enum serialization test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    test_users()
    test_posts()
    test_enum_serialization()


if __name__ == "__main__":
    main()