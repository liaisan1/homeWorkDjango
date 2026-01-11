import numpy as np

# 1. Массив 10x10 с min и max
arr1 = np.random.randint(0, 100, (10, 10))
print("1. Минимум:", arr1.min(), "Максимум:", arr1.max())

# 2. Массив 10x10 со средним по столбцам
arr2 = np.random.randint(0, 100, (10, 10))
print("\n2. Средние по столбцам:", arr2.mean(axis=0))

# 3. Вектор с заменой max на 0
vector = np.random.randint(0, 100, 10)
vector_modified = vector.copy()
vector_modified[np.argmax(vector)] = 0
print(f"\n3. Исходный: {vector}")
print(f"   Модифицированный: {vector_modified}")

# 4. Изменение знака у элементов между 3 и 8
arr4 = np.random.randint(0, 20, (5, 5))
mask = (arr4 > 3) & (arr4 < 8)
arr4[mask] = -arr4[mask]
print("\n4. Массив после изменения знака:")
print(arr4)