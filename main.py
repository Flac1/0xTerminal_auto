from collections import Counter
import json

def parse_json_input():
    lines = []
    print('Для получения JSON выполните следующие шаги: \n1. Зайдите в игру. \n2. Нажмите в браузере F12 (Откройте DevTools(Панель разработчиков) любым методом). \n3. Перейдите в раздел Network. \n4. Найдите объект с названием last. \n5. Скопируйте весь код, который находится во вкладке Response ')
    print('Если такого элемента нет, попробуйте выйти из текущего матча и зайти обратно. \nТакже, каждый новый матч нужно проделывать данный трюк еще раз с новым элементом last')
    print("\nВведите JSON (для завершения ввода нажмите Enter дважды):")
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    json_input = '\n'.join(lines)

    try:
        data = json.loads(json_input)
        words_list = data.get("words", [])
        return words_list

    except json.JSONDecodeError:
        print("Ошибка ввода JSON. Пожалуйста, введите корректный JSON.")
        return None

def keep_and_count_vertical_matching_words(sorted_matrix, first_word):
    first_word_letters = list(first_word)

    def count_vertical_matches(row):
        return sum(1 for i, letter in enumerate(row) if i < len(first_word_letters) and letter == first_word_letters[i])

    matching_matrix = []
    for row in sorted_matrix:
        vertical_matches = count_vertical_matches(row)
        matching_matrix.append(row + [vertical_matches])

    return matching_matrix

def dig_str_del(orig_string):
    final_string = ''
    for c in orig_string:
        if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            final_string = final_string + c
    return final_string

def dobavlenie_vesa(result_matrix, result_letter_counts):
    for row in result_matrix:
        row_sum = sum(result_letter_counts[var] for var in row)
        row.append(row_sum)
    return result_matrix

def count_letter_occurrences(matrix):
    # Используем Counter для подсчета количества букв
    letter_counts = Counter()

    # Итерируем по каждой букве в матрице
    for row in matrix:
        for letter in row:
            # Проверяем, является ли символ буквой
            if letter.isalpha():
                # Обновляем счетчик для данной буквы
                letter_counts[letter] += 1

    return letter_counts

def find_unique_letters(matrix):
    # Создаем множество для хранения уникальных букв
    unique_letters = set()

    # Итерируем по каждой букве в матрице
    for row in matrix:
        for letter in row:
            # Проверяем, является ли буква английской и добавляем в множество
            if letter.isalpha() and letter.isascii() and letter.isupper():
                unique_letters.add(letter)

    # Преобразуем множество в список и сортируем его
    alphabet = sorted(list(unique_letters))

    return alphabet

def print_matrix(matrix):
    for row in matrix:
        print(row)

def create_word_matrix(words):
    # Создаем пустую двумерную матрицу
    matrix = []

    # Заполняем матрицу буквами по словам
    for word in words:
        matrix.append(list(word))

    return matrix

def vibor_slova(sorted_matrix):
    choice1 = dig_str_del(str(''.join(str(el) for el in sorted_matrix[0]))) # Слово
    choice_result = input(f'\nВыберите слово {choice1} и введите количество совпадений по слову (число):')
    return choice_result

def kolvo_sovpad(sorted_matrix, kolvo_sovpad):
    print(sorted_matrix, kolvo_sovpad)
    return 0

def vivod_sovpad(sorted_matrix, kolvo_sovpad):
    filtered_matrix = []
    words_length = len(sorted_matrix[0]) - 1
    for word in sorted_matrix:
        if int(word[words_length]) == int(kolvo_sovpad):
            filtered_matrix.append(word)
    return filtered_matrix

def win():
    return 0

def main():

    activity_count = 0
    words_list = parse_json_input()

    # Шаг 1: Формируем матрицу из букв
    result_matrix = create_word_matrix(words_list)

    # Шаг 2: Определяем кол-во появлений букв в матрице
    result_letter_counts = count_letter_occurrences(result_matrix)

    # Шаг 3: Приписываем вес слова справа в матрице
    result_matrix = dobavlenie_vesa(result_matrix, result_letter_counts)
    sorted_matrix = sorted(result_matrix, key=lambda x: x[-1], reverse=True)
    print("\nОтсортированная матрица по весу слова в порядке убывания:")
    print_matrix(sorted_matrix)


    words_length = len(sorted_matrix[1]) - 1 # показывает настоящую длину слова и индекс числового параметра

    for row in sorted_matrix:
        row.pop(int(words_length))

    while True:

        # Шаг 4: Выбираем самое весомое слово для юзера
        activity_count += 1
        kolvo_sovpad = vibor_slova(sorted_matrix) # Число совпадений

        if int(kolvo_sovpad) == int(words_length):
            print('Вы выиграли')
            return 0
        print('Количество действий юзера произошло:', activity_count)
        if (activity_count == 4):
            print("Вы проиграли")
            return 0

        # Шаг 5: Убираем неподходящие слова из матрицы
        filtered_matrix = keep_and_count_vertical_matching_words(sorted_matrix, sorted_matrix[0])
        print('Матрица вариантов')
        sorted_matrix = vivod_sovpad(filtered_matrix, kolvo_sovpad)
        print_matrix(sorted_matrix)
        for row in sorted_matrix:
            row.pop(int(words_length))

if __name__ == '__main__':
    while True:
        main()
