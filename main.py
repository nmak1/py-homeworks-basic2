def read_cook_book(file_path):
    cook_book = {}
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
    return cook_book

# Пример использования
cook_book = read_cook_book('recipes.txt')
print(cook_book)

def get_shop_list_by_dishes(dishes, person_count, cook_book):
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
    return shop_list

# Пример использования
shop_list = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)
print(shop_list)

def merge_files(file_names, output_file):
    files_info = []
    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            files_info.append({
                'name': file_name,
                'line_count': len(lines),
                'content': lines
            })
    files_info.sort(key=lambda x: x['line_count'])
    with open(output_file, 'w', encoding='utf-8') as output:
        for file_info in files_info:
            output.write(f"{file_info['name']}\n{file_info['line_count']}\n")
            output.writelines(file_info['content'])

# Пример использования
file_names = ['1.txt', '2.txt']
merge_files(file_names, 'merged_file.txt')