import json
from typing import Dict, List, Any

class CookBook:
    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return self.path

    @staticmethod
    def read_cook_book(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        cook_book = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                while True:
                    dish_name = file.readline().strip()
                    if not dish_name:
                        break
                    ingredient_count = int(file.readline().strip())
                    ingredients = []
                    for _ in range(ingredient_count):
                        ingredient_info = file.readline().strip().split(' | ')
                        ingredient = {
                            'ingredient_name': ingredient_info[0],
                            'quantity': int(ingredient_info[1]),
                            'measure': ingredient_info[2]
                        }
                        ingredients.append(ingredient)
                    cook_book[dish_name] = ingredients
                    file.readline()  # Пропускаем пустую строку между рецептами
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
        return cook_book

    @staticmethod
    def get_shop_list_by_dishes(dishes: List[str], person_count: int, cook_book: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        shop_list = {}
        for dish in dishes:
            if dish in cook_book:
                for ingredient in cook_book[dish]:
                    ingredient_name = ingredient['ingredient_name']
                    measure = ingredient['measure']
                    quantity = ingredient['quantity'] * person_count
                    if ingredient_name in shop_list:
                        shop_list[ingredient_name]['quantity'] += quantity
                    else:
                        shop_list[ingredient_name] = {'measure': measure, 'quantity': quantity}
            else:
                print(f"Блюдо '{dish}' отсутствует в кулинарной книге.")
        return shop_list

class OutPut:
    @staticmethod
    def save_book(data: Any, file_path: str) -> None:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка при записи в файл: {e}")

    @staticmethod
    def load_book(file_path: str) -> Any:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except json.JSONDecodeError:
            print(f"Файл {file_path} имеет неверный формат JSON.")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

    @staticmethod
    def print_book(data: Any) -> None:
        print(json.dumps(data, ensure_ascii=False, indent=4))

class MergeFiles:
    @staticmethod
    def merge_files(file_names: List[str], output_file: str) -> None:
        files_info = []
        try:
            for file_name in file_names:
                try:
                    with open(file_name, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        files_info.append({
                            'name': file_name,
                            'line_count': len(lines),
                            'content': lines
                        })
                except FileNotFoundError:
                    print(f"Файл {file_name} не найден.")
                except Exception as e:
                    print(f"Ошибка при чтении файла {file_name}: {e}")

            files_info.sort(key=lambda x: x['line_count'])

            with open(output_file, 'w', encoding='utf-8') as output:
                for file_info in files_info:
                    output.write(f"{file_info['name']}\n{file_info['line_count']}\n")
                    output.writelines(file_info['content'])
        except IOError as e:
            print(f"Ошибка при записи в файл {output_file}: {e}")

# Пример использования
if __name__ == "__main__":
    cook_book = CookBook.read_cook_book('recipes.txt')
    OutPut.save_book(cook_book, 'cook_book.json')  # Сохраняем в JSON
    cook_book = OutPut.load_book('cook_book.json')  # Загружаем из JSON
    OutPut.print_book(cook_book)  # Красивый вывод

    shop_list =CookBook.get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)
    OutPut.save_book(shop_list, 'shop_list.json')  # Сохраняем в JSON
    shop_list = OutPut.load_book('shop_list.json')  # Загружаем из JSON
    OutPut.print_book(shop_list)

    file_names = ['1.txt', '2.txt']
    MergeFiles.merge_files(file_names, 'merged_file.txt')